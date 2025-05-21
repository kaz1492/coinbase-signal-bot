
import os
import requests

# Use the exact environment variable keys from Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(signal):
    try:
        if not TELEGRAM_TOKEN or not CHAT_ID:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in environment.")

        message = f"{signal['type']} signal for {signal['symbol']} [{signal['timeframe']}]: {signal['price']}"
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message}
        )
        response.raise_for_status()
        print("Message sent:", response.json())
    except Exception as e:
        print("Failed to send Telegram message:", e)
