
import requests

TELEGRAM_TOKEN = "7236197115:AAFFzBbjbeAHjNxo5VzFab61IxPXa5A2DEg"
CHAT_ID = "99455629"

try:
    message = "سیگنال تستی ارسال شد به صورت مستقیم با توکن واقعی"
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message}
    )
    response.raise_for_status()
    print("Message sent successfully:", response.json())
except Exception as e:
    print("Error sending message:", e)
