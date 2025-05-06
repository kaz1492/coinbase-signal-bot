import os
import asyncio
import logging
import requests
import pandas as pd
from telegram import Bot
from datetime import datetime

from indicators import calculate_indicators, check_signal, fetch_ohlcv

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

def get_coinbase_usd_pairs():
    url = "https://api.exchange.coinbase.com/products"
    response = requests.get(url)
    data = response.json()
    usd_pairs = [item["id"] for item in data if item["quote_currency"] == "USD"]
    return usd_pairs

async def main():
    pairs = get_coinbase_usd_pairs()
    granularities = {"15m": 900, "1h": 3600, "4h": 14400}
    for pair in pairs:
        for name, interval in granularities.items():
            df = fetch_ohlcv(pair, interval)
            if len(df) < 200:
                continue
            df = calculate_indicators(df)
            signal = check_signal(df)
            if signal:
                msg = f"Signal for {pair} on {name}:\n{signal}"
                await bot.send_message(chat_id=CHAT_ID, text=msg)
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
# تست دستی ارسال پیام
if __name__ == "__main__":
    import asyncio
    async def test():
        await bot.send_message(chat_id=CHAT_ID, text="Test signal from Coinbase bot.")
    asyncio.run(test())
