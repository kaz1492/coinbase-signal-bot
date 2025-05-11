
import os
from dotenv import load_dotenv
import requests
import json
import time

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_signal_to_telegram(signal):
    message = (
        f"رمزارز: {signal['symbol']}
"
        f"نوع سیگنال: {signal['type']}
"
        f"ورود: {signal['entry']}
"
        f"TP1: {signal['tp1']} | TP2: {signal['tp2']}
"
        f"TP3: {signal['tp3']} | TP4: {signal['tp4']}
"
        f"SL: {signal['sl']}
"
        f"اهرم: {signal['leverage']}
"
        f"تایم‌فریم: {signal['timeframe']}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, data=data)
    print("ارسال سیگنال:", response.status_code, response.text)

def load_signals():
    try:
        with open("signals.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print("خطا در خواندن signals.json:", e)
        return []

def main():
    print("ربات سیگنال آماده است...")
    while True:
        signals = load_signals()
        for signal in signals:
            send_signal_to_telegram(signal)
        time.sleep(60)  # تکرار هر 60 ثانیه

if __name__ == "__main__":
    main()
