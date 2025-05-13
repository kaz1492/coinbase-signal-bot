
import requests
import os
from dotenv import load_dotenv

# بارگذاری مقادیر از فایل .env
load_dotenv()

def send_telegram_signal(signal):
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    message = f"""
✅ New Signal
Type: {signal['type']}
Symbol: {signal['symbol']}
Entry: {signal['entry']}
Target: {signal['target1']}
Stoploss: {signal['stoploss']}
Leverage: {signal['leverage']}x
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Telegram Error:", response.text)
