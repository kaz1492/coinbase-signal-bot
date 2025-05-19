
from telegram import Bot

BOT_TOKEN = "8042153193:AAGLLK2SUi3dnVCwuN93mRzdbSuBGf1I3Vs"
CHAT_ID = "99455629"

bot = Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text="✅ تست موفقیت‌آمیز بود!")
