# Final version of signal bot
import os
import asyncio
from telegram import Bot
from signal_runner import run_signal_scan

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_message(msg):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

if __name__ == "__main__":
    asyncio.run(run_signal_scan(send_message))
