
import asyncio
from telegram import Bot

bot = Bot(token="7236197115:AAFFzBbjbeAHjNxo5VzFab61IxPXa5A2DEg")

async def test():
    await bot.send_message(chat_id="99455629", text="✅ بات به تلگرام متصل است!")

asyncio.run(test())
