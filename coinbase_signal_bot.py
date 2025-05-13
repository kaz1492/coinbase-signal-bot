
import time
from datetime import datetime
import requests
import os
import pandas as pd
from dotenv import load_dotenv

# بارگذاری توکن‌ها از .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# تابع ارسال پیام تلگرام
def send_telegram_signal(signal):
    message = (
        f"**Live Signal**\n"
        f"Pair: {signal['symbol']}\n"
        f"Type: {signal['type']}\n"
        f"Entry: {signal['entry']}\n"
        f"RSI: {signal['rsi']:.2f}\n"
        f"Target: {signal['target']}\n"
        f"Stoploss: {signal['stoploss']}\n"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# دریافت جفت ارزهای USD
def get_usd_pairs():
    url = "https://api.exchange.coinbase.com/products"
    response = requests.get(url)
    data = response.json()
    return [pair['id'] for pair in data if pair['quote_currency'] == 'USD' and pair['trading_disabled'] == False]

# دریافت داده تاریخی برای یک جفت
def get_candles(pair):
    url = f"https://api.exchange.coinbase.com/products/{pair}/candles?granularity=300"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
    df = df.sort_values("time")
    return df

# محاسبه RSI
def calculate_rsi(df, period=14):
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# منطق تحلیل و سیگنال‌دهی
def analyze_and_signal(pair):
    df = get_candles(pair)
    if df is None or df.shape[0] < 20:
        return
    df["rsi"] = calculate_rsi(df)
    latest = df.iloc[-1]
    rsi = latest["rsi"]

    if rsi < 30:
        signal = {
            "symbol": pair,
            "type": "Buy",
            "entry": latest["close"],
            "rsi": rsi,
            "target": round(latest["close"] * 1.03, 6),
            "stoploss": round(latest["close"] * 0.97, 6)
        }
        send_telegram_signal(signal)
    elif rsi > 70:
        signal = {
            "symbol": pair,
            "type": "Sell",
            "entry": latest["close"],
            "rsi": rsi,
            "target": round(latest["close"] * 0.97, 6),
            "stoploss": round(latest["close"] * 1.03, 6)
        }
        send_telegram_signal(signal)

# حلقه اصلی
def main():
    print("Started live RSI-based signal bot...")
    while True:
        try:
            pairs = get_usd_pairs()
            for pair in pairs:
                analyze_and_signal(pair)
            time.sleep(180)  # هر 3 دقیقه
        except Exception as e:
            print("Error:", e)
            time.sleep(30)

if __name__ == "__main__":
    main()
