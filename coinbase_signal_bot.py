
import time
from datetime import datetime
from telegram_sender import send_telegram_signal  # فرض بر این است که این تابع قبلاً ساخته شده

def fetch_market_data():
    # دریافت اطلاعات بازار از Coinbase یا API دیگر
    return {
        "symbol": "B3/USD",
        "price": 0.005608,
        "volume": 350000,
    }

def analyze_signal(data):
    # تحلیل شرایط صدور سیگنال
    if data["price"] > 0.0056:
        return {
            "type": "Buy",
            "symbol": data["symbol"],
            "entry": data["price"],
            "target1": round(data["price"] * 1.05, 6),
            "stoploss": round(data["price"] * 0.95, 6),
            "leverage": 5
        }
    return None

def main():
    print("Real-time signal system started...")
    while True:
        try:
            data = fetch_market_data()
            signal = analyze_signal(data)
            if signal:
                send_telegram_signal(signal)
                print(f"Signal sent at {datetime.utcnow()} - {signal}")
            time.sleep(30)  # بررسی هر 30 ثانیه
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
