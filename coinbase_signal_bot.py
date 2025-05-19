
import os
import asyncio
import json
import time
import requests
import websockets
import pandas as pd
from telegram import Bot
from collections import defaultdict

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

USD_PAIRS = ["BTC-USD", "ETH-USD", "SOL-USD"]

order_volume_window = defaultdict(list)
VOLUME_THRESHOLD = 100000
sent_signals = {}

def get_candles(symbol, granularity):
    url = f"https://api.exchange.coinbase.com/products/{symbol}/candles?granularity={granularity}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
        df = df.sort_values("time").reset_index(drop=True)
        return df
    return None

async def send_signal(symbol, entry_price, signal_type, score):
    tp_factors = [1.05, 1.10, 1.20, 1.30] if signal_type == "LONG" else [0.95, 0.90, 0.85, 0.80]
    sl_factor = 0.975 if signal_type == "LONG" else 1.025
    targets = [round(entry_price * f, 6) for f in tp_factors]
    sl = round(entry_price * sl_factor, 6)

    msg = f"{signal_type} SIGNAL - {symbol}
"
    msg += f"Entry Price: {entry_price}
"
    msg += "Targets:
"
    msg += f"• TP1: {targets[0]}
"
    msg += f"• TP2: {targets[1]}
"
    msg += f"• TP3: {targets[2]}
"
    msg += f"• TP4: {targets[3]}
"
    msg += f"Stop Loss: {sl}
"
    msg += f"Confidence Score: {score}/5"

    print("Trying to send message:", msg)
    await bot.send_message(chat_id=CHAT_ID, text=msg)

def prune_old_orders(pair):
    current_time = time.time()
    order_volume_window[pair] = [(ts, usd) for ts, usd in order_volume_window[pair] if current_time - ts < 60]

def check_smart_money(pair):
    prune_old_orders(pair)
    total_usd = sum(usd for _, usd in order_volume_window[pair])
    return total_usd > VOLUME_THRESHOLD

async def analyze_and_signal(symbol, price):
    df_4h = get_candles(symbol, 14400)
    if df_4h is None:
        return

    latest = df_4h.iloc[-1]
    signal_type = None
    if latest["close"] > latest["open"]:
        signal_type = "LONG"
    elif latest["close"] < latest["open"]:
        signal_type = "SHORT"

    score = 5

    if signal_type:
        await send_signal(symbol, price, signal_type, score)

async def handle_message(message):
    data = json.loads(message)
    if data["type"] == "match":
        symbol = data.get("product_id")
        size = float(data.get("size", 0))
        price = float(data.get("price", 0))
        usd_value = size * price
        order_volume_window[symbol].append((time.time(), usd_value))

        if check_smart_money(symbol):
            await analyze_and_signal(symbol, price)

async def subscribe(ws):
    await ws.send(json.dumps({
        "type": "subscribe",
        "product_ids": USD_PAIRS,
        "channels": ["full"]
    }))

async def main():
    async with websockets.connect("wss://ws-feed.exchange.coinbase.com") as ws:
        await subscribe(ws)
        while True:
            try:
                msg = await ws.recv()
                await handle_message(msg)
            except Exception as e:
                print("Error:", e)
                break

if __name__ == "__main__":
    asyncio.run(main())
