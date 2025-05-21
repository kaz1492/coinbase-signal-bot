
import pandas as pd
from utils import calculate_rsi, calculate_ma
from delta_analyzer import analyze_delta
from lux_smc_engine import analyze_smc
from telegram_sender import send_to_telegram

def generate_signal(df, symbol, timeframe):
    try:
        signal = {}

        df['rsi'] = calculate_rsi(df['close'])
        df['ma20'] = calculate_ma(df['close'], window=20)

        rsi_last = df['rsi'].iloc[-1]
        ma_last = df['ma20'].iloc[-1]
        price_last = df['close'].iloc[-1]

        print(f"[{symbol} - {timeframe}] RSI: {rsi_last}, MA20: {ma_last}, Price: {price_last}")

        if rsi_last < 30 and price_last > ma_last:
            signal['type'] = 'BUY'
        elif rsi_last > 70 and price_last < ma_last:
            signal['type'] = 'SELL'
        else:
            print(f"[{symbol} - {timeframe}] No signal conditions met.")
            return None

        delta = analyze_delta(df)
        smc = analyze_smc(df)

        signal['symbol'] = symbol
        signal['timeframe'] = timeframe
        signal['price'] = price_last
        signal['delta_divergence'] = delta
        signal['smc_pattern'] = smc

        print(f"[{symbol} - {timeframe}] Signal generated: {signal}")
        send_to_telegram(signal)
        return signal
    except Exception as e:
        print(f"[{symbol} - {timeframe}] ERROR in signal generation:", e)
        return None
