import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pandas as pd
import numpy as np
import talib
import ccxt
import sqlite3
import logging
from datetime import datetime
from src.notification.telegram_sender import send_telegram_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_db():
    conn = sqlite3.connect('src/database/signals.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS backtest_results
                 (pair TEXT, signal_type TEXT, entry REAL, tps TEXT, sl REAL, result TEXT,
                  profit REAL, timestamp TEXT)''')
    conn.commit()
    conn.close()

def fetch_historical_data(pair, timeframe='15m', since='2024-05-01'):
    try:
        exchange = ccxt.coinbasepro()
        since_ts = exchange.parse8601(since)
        ohlcv = exchange.fetch_ohlcv(pair, timeframe, since_ts, limit=1000)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['buy_volume'] = df['volume'] * 0.6
        df['sell_volume'] = df['volume'] * 0.4
        return df
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def generate_signal(row, prev_rows, atr):
    delta = row['buy_volume'] - row['sell_volume']
    close_prices = prev_rows['close'].values
    if len(close_prices) < 14:
        return None, delta, 50
    
    rsi = talib.RSI(close_prices, timeperiod=14)[-1]
    signal = None
    if rsi < 30 and delta < 0 and row['buy_volume'] > row['sell_volume'] * 1.2:
        signal = 'long'
    elif rsi > 70 and delta > 0 and row['sell_volume'] > row['buy_volume'] * 1.2:
        signal = 'short'
    return signal, delta, rsi

def evaluate_trade(entry_price, signal_type, tps, sl, future_prices, leverage=10):
    for price in future_prices:
        if signal_type == 'long':
            if price >= tps[0]:
                profit = (tps[0] - entry_price) / entry_price * 100 * leverage
                return 'win', profit
            elif price <= sl:
                profit = (sl - entry_price) / entry_price * 100 * leverage
                return 'loss', profit
        else:
            if price <= tps[0]:
                profit = (entry_price - tps[0]) / entry_price * 100 * leverage
                return 'win', profit
            elif price >= sl:
                profit = (entry_price - sl) / entry_price * 100 * leverage
                return 'loss', profit
    return 'open', 0

def run_backtest(pair='FIL/USD', timeframe='15m', start_date='2024-05-01'):
    init_db()
    data = fetch_historical_data(pair, timeframe, start_date)
    if data.empty:
        logging.error("No data available for backtest")
        return "No data", 0, 0
    
    tp_percents = [0.015, 0.03, 0.05, 0.08]
    sl_percent = 0.025
    results = []
    wins = 0
    total_trades = 0
    total_profit = 0

    for i in range(14, len(data) - 10):
        row = data.iloc[i]
        prev_rows = data.iloc[i-14:i]
        
        highs = prev_rows['high'].values
        lows = prev_rows['low'].values
        closes = prev_rows['close'].values
        atr = talib.ATR(highs, lows, closes, timeperiod=14)[-1] if len(highs) >= 14 else 0.02
        
        signal, delta, rsi = generate_signal(row, prev_rows, atr)
        if not signal:
            continue
            
        entry_price = row['close']
        if signal == 'long':
            tps = [entry_price * (1 + p) for p in tp_percents]
            sl = entry_price * (1 - sl_percent)
        else:
            tps = [entry_price * (1 - p) for p in tp_percents]
            sl = entry_price * (1 + sl_percent)
        
        future_prices = data.iloc[i+1:i+11]['close'].values
        result, profit = evaluate_trade(entry_price, signal, tps, sl, future_prices)
        
        if result != 'open':
            total_trades += 1
            if result == 'win':
                wins += 1
            total_profit += profit
            
            conn = sqlite3.connect('src/database/signals.db')
            c = conn.cursor()
            c.execute('INSERT INTO backtest_results VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (pair, signal, entry_price, str(tps), sl, result, profit, row['timestamp'].isoformat()))
            conn.commit()
            conn.close()
            
            results.append({
                'pair': pair,
                'signal': signal,
                'entry': entry_price,
                'result': result,
                'profit': profit,
                'timestamp': row['timestamp']
            })

    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    report = f"""
Backtest Report for {pair} ({timeframe})
Total Trades: {total_trades}
Win Rate: {win_rate:.2f}%
Total Profit: {total_profit:.2f}%
Average Profit per Trade: {(total_profit / total_trades):.2f}% (if trades > 0)
"""
    logging.info(report)
    send_telegram_message(report)
    pd.DataFrame(results).to_csv(f'backtest_results_{pair.replace("/", "_")}.csv', index=False)
    return report, win_rate, total_profit

if __name__ == "__main__":
    run_backtest(pair='FIL/USD', timeframe='15m')
