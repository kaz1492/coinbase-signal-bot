
import requests
import json

TELEGRAM_TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_to_telegram(signal):
    msg = f"{signal['type']} signal for {signal['symbol']} [{signal['timeframe']}]: {signal['price']}"
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )
