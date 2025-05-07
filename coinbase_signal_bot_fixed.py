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
        df = df.sort_values("time")
        return df
    return None

async def check_signal():
    while True:
        for pair in USD_PAIRS:
            df = get_candles(pair, 900)  # 15 minutes
            if df is not None:
                signal = calculate_indicators(df)
                if signal and pair not in sent_signals:
                    entry = df["close"].iloc[-1]
                    direction = "خرید" if signal == "long" else "فروش"
                    emoji = "✅" if signal == "long" else "❌"
                    text = f"{pair} - سیگنال {direction} 📢\nورود: {entry:.4f} {emoji}\n🎯 تارگت‌ها:\n"
                    if signal == "long":
                        tps = [entry * 1.015, entry * 1.03, entry * 1.05, entry * 1.08]
                        sl = entry * 0.975
                    else:
                        tps = [entry * 0.985, entry * 0.97, entry * 0.95, entry * 0.92]
                        sl = entry * 1.025
                    for i, tp in enumerate(tps, 1):
                        text += f"• TP{i}: {tp:.4f}\n"
                    text += f"❌ استاپ لاس: {sl:.4f}"
                    bot.send_message(chat_id=CHAT_ID, text=text)
                    sent_signals[pair] = time.time()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(check_signal())
