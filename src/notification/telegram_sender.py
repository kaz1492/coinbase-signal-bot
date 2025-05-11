import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: BOT_TOKEN or CHAT_ID not set in .env")
        return 500, "Missing environment variables"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        print(f"Telegram response status: {response.status_code}")
        return response.status_code, response.text
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return 500, str(e)