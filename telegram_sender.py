# telegram_sender.py
# Sends signal messages to Telegram via Bot API

import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_signal(signal):
    message = f"""
{signal['pair']} ({signal['timeframe']}) - {signal['direction']}
Entry: {signal['entry']}
Targets:
TP1: {signal['targets'][0]}
TP2: {signal['targets'][1]}
TP3: {signal['targets'][2]}
TP4: {signal['targets'][3]}
SL: {signal['stop_loss']}
Leverage: {signal['leverage']}x
Win Rate: {signal['win_rate']}%
"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message.strip()
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")
