import os
import asyncio
import json
import time
import requests
import websockets
from collections import defaultdict
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

USD_PAIRS = [
    "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "AVAX-USD", "LINK-USD", "MATIC-USD", "DOGE-USD", "LTC-USD", "BCH-USD",
    "DOT-USD", "ATOM-USD", "XLM-USD", "AAVE-USD", "ETC-USD", "NEAR-USD", "SAND-USD", "ICP-USD", "GRT-USD", "RUNE-USD",
    "UNI-USD", "FIL-USD", "ALGO-USD", "EGLD-USD", "CRO-USD", "FTM-USD", "XTZ-USD", "RNDR-USD", "IMX-USD", "ARB-USD"
]

order_volume_window = defaultdict(list)
VOLUME_THRESHOLD = 100000

def prune_old_orders(pair):
    current_time = time.time()
    order_volume_window[pair] = [
        (ts, usd) for ts, usd in order_volume_window[pair] if current_time - ts < 15
    ]

def check_smart_money(pair):
    prune_old_orders(pair)
    total_usd = sum(usd for _, usd in order_volume_window[pair])
    return total_usd > VOLUME_THRESHOLD

def get_15m_candles(product_id):
    url = f"https://api.exchange.coinbase.com/products/{product_id}/candles?granularity=900"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def analyze_candles(candles):
    if len(candles) < 2:
        return None
    last = candles[0]
    prev = candles[1]
    _, high, low, close, _ = last
    _, ph, pl, pc, _ = prev

    if close > pc and close > high - (high - low) * 0.3:
        return "LONG"
    elif close < pc and close < low + (high - low) * 0.3:
        return "SHORT"
    return None

async def send_signal(symbol, entry_price, signal_type):
    tp1 = round(entry_price * (1.015 if signal_type == "LONG" else 0.985), 4)
    tp2 = round(entry_price * (1.03 if signal_type == "LONG" else 0.97), 4)
    tp3 = round(entry_price * (1.05 if signal_type == "LONG" else 0.95), 4)
    tp4 = round(entry_price * (1.08 if signal_type == "LONG" else 0.92), 4)
    sl = round(entry_price * (0.975 if signal_type == "LONG" else 1.025), 4)

    msg = f"📊 سیگنال {signal_type} - {symbol}\n"
    msg += f"✅ قیمت ورود: {entry_price}\n"
    msg += f"🎯 TP1: {tp1}\n🎯 TP2: {tp2}\n🎯 TP3: {tp3}\n🎯 TP4: {tp4}\n"
    msg += f"❌ SL: {sl}"

    await bot.send_message(chat_id=CHAT_ID, text=msg)

async def subscribe(ws):
    message = {
        "type": "subscribe",
        "product_ids": USD_PAIRS,
        "channels": ["full"]
    }
    await ws.send(json.dumps(message))

async def handle_message(message):
    data = json.loads(message)
    if data["type"] == "match":
        product = data.get("product_id", "")
        size = float(data.get("size", 0))
        price = float(data.get("price", 0))
        usd_value = size * price
        order_volume_window[product].append((time.time(), usd_value))

        if check_smart_money(product):
            candles = get_15m_candles(product)
            signal = analyze_candles(candles)
            if signal:
                await send_signal(product, price, signal)
            order_volume_window[product] = []

async def main():
    url = "wss://ws-feed.exchange.coinbase.com"
    async with websockets.connect(url) as ws:
        await subscribe(ws)
        while True:
            try:
                msg = await ws.recv()
                await handle_message(msg)
            except Exception as e:
                print("خطا:", e)
                break

if __name__ == "__main__":
    asyncio.run(main())