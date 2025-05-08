
import requests

BOT_TOKEN = "8042153193:AAHduu2kNtc5F-oZ5H0_K2vcLqUr4Hvw8EY"
CHAT_ID = "99455629"  # Chat ID تأییدشده از سمت کاربر

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    print(f"Telegram response status: {response.status_code}")
    print(f"Telegram response text: {response.text}")
    return response.status_code, response.text
