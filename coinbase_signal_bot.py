import os
import asyncio
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

async def send_signal():
    signal_type = "خرید"
    symbol = "BTC/USD"
    entry_price = 62000
    tp1 = round(entry_price * 1.015, 2)
    tp2 = round(entry_price * 1.03, 2)
    tp3 = round(entry_price * 1.05, 2)
    tp4 = round(entry_price * 1.08, 2)
    sl = round(entry_price * 0.975, 2)

    message = (
        f"📢 سیگنال {signal_type.upper()} - {symbol}\n"
        f"✅ ورود: {entry_price}\n"
        f"🎯 تارگت‌ها:\n"
        f"• TP1: {tp1}\n"
        f"• TP2: {tp2}\n"
        f"• TP3: {tp3}\n"
        f"• TP4: {tp4}\n"
        f"❌ استاپ لاس: {sl}"
    )

    await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    asyncio.run(send_signal())