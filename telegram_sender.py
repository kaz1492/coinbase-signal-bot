import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signal_message(symbol, signal, timeframe):
    message = f"{symbol} [{timeframe}]\nSignal: {signal['type']}\nEntry: {signal['entry']}\nTP1: {signal['tp1']} TP2: {signal['tp2']}\nSL: {signal['sl']}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)