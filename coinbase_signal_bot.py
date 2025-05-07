
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
    "BTC-USD", "ETH-USD", "SOL-USD",
    "DOT-USD", "ATOM-USD", "XLM-USD",
    "UNI-USD", "FIL-USD", "ALGO-USD"
]

order_volume_window = defaultdict(list)
VOLUME_THRESHOLD = 100000  # USD in volume
sent_signals = {}  # timestamp control

def get_candles(symbol, granularity):
    url = f"https://api.exchange.coinbase.com/products/{symbol}/candles?granularity={granularity}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.sort_values("time", inplace=True)
        return df
    return None

async def analyze_market():
    while True:
        for pair in USD_PAIRS:
            df = get_candles(pair, 900)
            if df is not None:
                signal = calculate_indicators(df)
                if signal:
                    entry = df["close"].iloc[-1]
                    if signal == "buy":
                        tp1 = round(entry * 1.015, 4)
                        tp2 = round(entry * 1.03, 4)
                        tp3 = round(entry * 1.05, 4)
                        tp4 = round(entry * 1.08, 4)
                        sl = round(entry * 0.975, 4)
                        text = f"{pair} - سیگنال خرید  
ورود: {entry} ✅
تارگت‌ها: 🎯
• TP1: {tp1}
• TP2: {tp2}
• TP3: {tp3}
• TP4: {tp4}
❌ استاپ لاس: {sl}"
                        bot.send_message(chat_id=CHAT_ID, text=text)
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(send_status_report())
    await analyze_market()

async def send_status_report():
    while True:
        try:
            bot.send_message(chat_id=CHAT_ID, text="ربات فعال است ✅ هنوز سیگنال جدیدی شناسایی نشده.")
        except Exception as e:
            print("خطا در ارسال گزارش وضعیت:", e)
        await asyncio.sleep(1800)

if __name__ == "__main__":
    asyncio.run(main())
