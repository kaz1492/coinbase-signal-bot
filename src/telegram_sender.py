
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signal_to_telegram(signal):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not set.")
        return

    message = (
        f"**{signal['pair']} [{signal['timeframe']}] - {signal['type']} Signal**\n"
        f"Entry: {signal['entry']}\n"
        f"Targets:\n"
        f"- TP1: {signal['tp1']}\n"
        f"- TP2: {signal['tp2']}\n"
        f"- TP3: {signal['tp3']}\n"
        f"- TP4: {signal['tp4']}\n"
        f"Stop Loss: {signal['sl']}\n"
        f"Leverage: {signal['leverage']}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Telegram Error: {response.text}")
    except Exception as e:
        print(f"Telegram Exception: {e}")
