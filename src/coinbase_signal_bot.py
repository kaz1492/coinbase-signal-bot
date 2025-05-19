
import os
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

async def test_send():
    await bot.send_message(chat_id=CHAT_ID, text="Bot is connected and working!")

# For direct execution during deployment or testing
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_send())
