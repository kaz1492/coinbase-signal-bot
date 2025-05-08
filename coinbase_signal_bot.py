
from delta_analyzer import DeltaAnalyzer
import datetime

analyzer = DeltaAnalyzer()

# در اینجا فرض شده است که تریدها به صورت real-time دریافت می‌شوند
# به عنوان مثال:
analyzer.process_trade(price=2.57, size=100, side="buy", timestamp=datetime.datetime.utcnow())
analyzer.process_trade(price=2.58, size=120, side="sell", timestamp=datetime.datetime.utcnow())

start = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
end = datetime.datetime.utcnow()

delta, buy, sell = analyzer.calculate_candle_delta(start, end)

# برای ارسال به تلگرام
signal_message = f"""
FIL-USD – سیگنال احتمالی
تایم‌فریم: 15m
دلتا کل: {delta:.2f}
خرید: {buy:.2f} / فروش: {sell:.2f}
"""

print(signal_message)


from telegram_sender_updated import send_telegram_message
send_telegram_message(signal_message)
