
from coinbase_ws_listener import CoinbaseWebSocket
from telegram_sender import send_telegram_message
import time

# جفت‌ارز مورد نظر
product_id = "FIL-USD"

# ساخت WebSocket و اجرای آن
ws_client = CoinbaseWebSocket(product_id=product_id)
ws_client.run()

# اجرای لوپ تحلیل هر 1 دقیقه
while True:
    time.sleep(60)  # هر 1 دقیقه یک‌بار تحلیل کندل
    signal = ws_client.get_latest_delta_signal()
    if signal:
        message = f"{product_id} – هشدار دلتا (15m)\n{signal}"
        status, resp = send_telegram_message(message)
        print(f"سیگنال ارسال شد: {status} | پاسخ: {resp}")
