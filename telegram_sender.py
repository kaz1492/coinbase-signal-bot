import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signal_message(symbol, signal, timeframe):
    message = (
        f"🚀 <b>{symbol} [{timeframe}]</b>\n"
        f"Type: <b>{signal['type']}</b>\n"
        f"Entry: <code>{signal['entry']}</code>\n"
        f"TP1: {signal['tp1']}\nTP2: {signal['tp2']}\nTP3: {signal['tp3']}\nTP4: {signal['tp4']}\n"
        f"SL: {signal['sl']}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)