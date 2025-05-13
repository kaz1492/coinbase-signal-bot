
import time
from datetime import datetime
from telegram_sender import send_telegram_signal

def main():
    print("Testing signal delivery every 20 seconds...")
    count = 1
    while True:
        signal = {
            "type": "Test",
            "symbol": "B3/USD",
            "entry": 0.005600 + count * 0.000001,
            "target1": 0.005800,
            "stoploss": 0.005400,
            "leverage": 3
        }
        print(f"Sending test signal {count} at", datetime.utcnow())
        send_telegram_signal(signal)
        count += 1
        time.sleep(20)

if __name__ == "__main__":
    main()
