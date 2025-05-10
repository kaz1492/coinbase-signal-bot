import requests

TELEGRAM_TOKEN = "8176087703:AAH4-qlUDUuoiXWTAWLaKLu61PK7jJZLZ-A"
CHAT_ID = "99455629"

message = "✅ پیام تست از ربات سیگنال - اتصال موفق بود!"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "HTML"
}

response = requests.post(url, data=payload)
print("Status:", response.status_code)
print("Response:", response.text)