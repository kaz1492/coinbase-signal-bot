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
    "UNI-USD", "FIL-USD", "ALGO-USD"
]

order_volume_window = defaultdict(list)
VOLUME_THRESHOLD = 100000  # USD in volume

async def analyze_pair(pair):
    url = f"wss://ws-feed.exchange.coinbase.com"
    subscribe_message = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": [pair]}]
    }

    async with websockets.connect(url) as ws:
        await ws.send(json.dumps(subscribe_message))
        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(message)
                if "price" in data and "volume_24h" in data:
                    price = float(data["price"])
                    volume = float(data["volume_24h"])
                    order_volume_window[pair].append(volume)
                    if len(order_volume_window[pair]) > 3:
                        order_volume_window[pair].pop(0)
                    avg_volume = sum(order_volume_window[pair]) / len(order_volume_window[pair])
                    if volume > avg_volume * 1.2 and volume > VOLUME_THRESHOLD:
                        await send_signal(pair, price, "buy")
            except Exception as e:
                print(f"Error in analyze_pair {pair}: {e}")
                continue

async def send_signal(pair, entry_price, signal_type):
    entry = round(entry_price, 4)
    if signal_type == "buy":
        tp1 = round(entry * 1.015, 4)
        tp2 = round(entry * 1.03, 4)
        tp3 = round(entry * 1.05, 4)
        tp4 = round(entry * 1.08, 4)
        sl = round(entry * 0.975, 4)
        text = f"{pair} - BUY SIGNAL\nEntry: {entry}\nTargets:\nTP1: {tp1}\nTP2: {tp2}\nTP3: {tp3}\nTP4: {tp4}\nSTOP LOSS: {sl}"
        await bot.send_message(chat_id=CHAT_ID, text=text)

async def main():
    tasks = [analyze_pair(pair) for pair in USD_PAIRS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())