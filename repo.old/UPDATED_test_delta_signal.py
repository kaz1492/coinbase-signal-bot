
from telegram_sender import send_telegram_message

# پیام تستی دلتا برای بررسی ارسال به تلگرام
message = """
FIL-USD – <b>هشدار تستی دلتا (15m)</b>
دلتا: -85.72
حجم خرید: 190.3
حجم فروش: 276.0

⚠️ احتمال برگشت قیمت از ناحیه کف
"""

# ارسال
status, resp = send_telegram_message(message)
print(f"پیام تستی ارسال شد! وضعیت: {status}")
