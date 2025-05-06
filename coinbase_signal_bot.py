
import os
import requests
from datetime import datetime

# جایگزین این کد با نسخه نهایی تولید شده در پاسخ کامل باشد
# در نسخه واقعی: تحلیل تمام USD pairs، محاسبه MA50/200، RSI، سیگنال‌دهی و ارسال به تلگرام

def send_telegram_message(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def simulate_signal():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    entry = 0.0055
    tp1 = entry * 1.015
    tp2 = entry * 1.03
    tp3 = entry * 1.05
    tp4 = entry * 1.08
    sl = entry * 0.975
    msg = (
        f"📢 سیگنال خرید (Long) - BTC/USD
"
        f"⏱ تایم‌فریم: 15 دقیقه
"
        f"📌 قیمت ورود: {entry:.6f}
"
        f"🎯 تارگت‌ها:
"
        f"1️⃣ {tp1:.6f}
2️⃣ {tp2:.6f}
3️⃣ {tp3:.6f}
4️⃣ {tp4:.6f}
"
        f"❌ حد ضرر: {sl:.6f}
"
        f"🕒 زمان تحلیل: {now}"
    )
    send_telegram_message(msg)

if __name__ == "__main__":
    simulate_signal()
