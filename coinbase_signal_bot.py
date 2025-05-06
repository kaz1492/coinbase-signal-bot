import asyncio
import requests
from indicators import calculate_indicators, check_signal, fetch_ohlcv
from telegram import Bot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

async def main():
    pairs = ["BTC-USD", "ETH-USD"]
    timeframes = {"15m": 900, "1h": 3600, "4h": 14400}

    for pair in pairs:
        for name, interval in timeframes.items():
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
