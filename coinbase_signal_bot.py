
import os
import asyncio
import json
import time
import requests
import websockets
import pandas as pd
from telegram import Bot
from collections import defaultdict
from indicators import calculate_indicators

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

USD_PAIRS = [
    "BTC-USD", "ETH-USD", "SOL-USD", "DOT-USD", "ATOM-USD", "XLM-USD",
    "UNI-USD", "FIL-USD", "ALGO-USD", "RNDR-USD"
]

order_volume_window = defaultdict(list)
VOLUME_THRESHOLD = 100000  # USD
sent_signals = {}

def get_candles(symbol, granularity):
    url = f"https://api.exchange.coinbase.com/products/{symbol}/candles?granularity={granularity}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df.sort_values("time")
    return None

def send_signal(pair, signal_type, entry_price, tp1, tp2, tp3, tp4, sl):
    signal_key = f"{pair}_{signal_type}_{entry_price}"
    if sent_signals.get(signal_key):
        return  # Already sent
    text = f"""{pair} - سیگنال {'خرید' if signal_type == 'Buy' else 'فروش'} 
ورود: {entry_price}
🎯 تارگت‌ها:
• TP1: {tp1}
• TP2: {tp2}
• TP3: {tp3}
• TP4: {tp4}
❌ استاپ لاس: {sl}"""
    bot.send_message(chat_id=CHAT_ID, text=text)
    sent_signals[signal_key] = True

async def monitor():
    while True:
        for pair in USD_PAIRS:
            df = get_candles(pair, 900)  # 15m
            if df is not None and len(df) > 50:
                entry = df.iloc[-1]["close"]
                signal_type = "Buy"
                tp1 = round(entry * 1.015, 4)
                tp2 = round(entry * 1.03, 4)
                tp3 = round(entry * 1.05, 4)
                tp4 = round(entry * 1.08, 4)
                sl = round(entry * 0.975, 4)
                send_signal(pair, signal_type, entry, tp1, tp2, tp3, tp4, sl)
        await asyncio.sleep(60)

asyncio.run(monitor())
