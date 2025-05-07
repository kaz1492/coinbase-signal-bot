
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
VOLUME_THRESHOLD = 100000  # USD in volume
sent_signals = {}  # timestamp control

def get_candle_signal(symbol, entry):
    tp1 = round(entry * 1.015, 4)
    tp2 = round(entry * 1.03, 4)
    tp3 = round(entry * 1.05, 4)
    tp4 = round(entry * 1.08, 4)
    sl = round(entry * 0.975, 4)
    text = f"""{symbol} - سیگنال خرید
ورود: {entry}
تارگت‌ها:
• TP1: {tp1}
• TP2: {tp2}
• TP3: {tp3}
• TP4: {tp4}
استاپ لاس: {sl}"""
    return text

# مثال ارسال سیگنال
async def send_sample_signal():
    text = get_candle_signal("RNDR-USD", 4.2342)
    await bot.send_message(chat_id=CHAT_ID, text=text)

if __name__ == "__main__":
    asyncio.run(send_sample_signal())
