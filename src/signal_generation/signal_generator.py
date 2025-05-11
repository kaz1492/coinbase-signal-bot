import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.analysis.technical_analyzer import TechnicalAnalyzer
from src.notification.telegram_sender import send_telegram_message
from datetime import datetime, timedelta
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_db():
    conn = sqlite3.connect('src/database/signals.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS signals 
                 (pair TEXT, type TEXT, entry REAL, tps TEXT, sl REAL, leverage TEXT, timeframe TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_signal_to_db(pair, signal_type, entry, tps, sl, leverage, timeframe):
    conn = sqlite3.connect('src/database/signals.db')
    c = conn.cursor()
    c.execute('INSERT INTO signals VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (pair, signal_type, entry, str(tps), sl, leverage, timeframe, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def generate_signal(pair, timeframe="15m"):
    init_db()
    analyzer = TechnicalAnalyzer()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=15)
    
    trades = analyzer.delta_analyzer.order_data
    result = analyzer.analyze(trades, start_time, end_time)
    
    if not result["signal"]:
        return None
        
    signal_type = result["signal"]
    entry = trades[-1]["price"] if trades else 0
    atr = result["atr"]
    
    tp_percents = [0.015, 0.03, 0.05, 0.08]
    sl_percent = min(0.025, atr * 1.5 / entry)
    
    if signal_type == "long":
        tps = [entry * (1 + p) for p in tp_percents]
        sl = entry * (1 - sl_percent)
    else:
        tps = [entry * (1 - p) for p in tp_percents]
        sl = entry * (1 + sl_percent)
    
    volatility = tp_percents[-1] + sl_percent
    leverage = "x3" if volatility < 0.05 else "x5" if volatility < 0.08 else "x10" if volatility < 0.12 else "x20"
    
    direction = "خرید" if signal_type == "long" else "فروش"
    message = f"{pair} – سیگنال {direction} (فیوچرز)\n\n"
    message += f"ورود: {entry:.4f}\nاهرم: {leverage} – Isolated\nتایم‌فریم: {timeframe}\n\n🎯 تارگت‌ها:"
    for i, tp in enumerate(tps, 1):
        percent = tp_percents[i-1] * 100
        message += f"\n• TP{i}: {tp:.4f} ({'+' if signal_type=='long' else '-'}{percent:.1f}%)"
    message += f"\n\n❌ استاپ لاس: {sl:.4f} ({'-' if signal_type=='long' else '+'}{sl_percent*100:.1f}%)"
    message += "\n\nتحلیل: دلتا + RSI + MACD"
    
    save_signal_to_db(pair, signal_type, entry, tps, sl, leverage, timeframe)
    status, _ = send_telegram_message(message)
    if status != 200:
        logging.error(f"Failed to send signal for {pair}: {status}")
        send_telegram_message(f"خطا در ارسال سیگنال {pair}! وضعیت: {status}")
    
    return message
