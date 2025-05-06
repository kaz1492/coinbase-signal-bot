import os
import requests
import pandas as pd
from telegram import Bot
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "99455629"
bot = Bot(token=TOKEN)

def get_coinbase_usd_pairs():
    url = "https://api.exchange.coinbase.com/products"
    response = requests.get(url)
    data = response.json()
    usd_pairs = [item["id"] for item in data if item["quote_currency"] == "USD"]
    return usd_pairs

def fetch_ohlcv(pair, granularity):
    url = f"https://api.exchange.coinbase.com/products/{pair}/candles?granularity={granularity}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
    df = df.sort_values("time")
    df["ma50"] = df["close"].rolling(window=50).mean()
    df["ma200"] = df["close"].rolling(window=200).mean()
    df["rsi"] = compute_rsi(df["close"], 14)
    return df

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def check_signal(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    signal = ""
    if prev["ma50"] < prev["ma200"] and last["ma50"] > last["ma200"]:
        signal += "Golden Cross | "
    if last["rsi"] < 30:
        signal += "RSI Oversold | "
    if last["rsi"] > 70:
        signal += "RSI Overbought | "
    return signal.strip(" | ")

def main():
    pairs = get_coinbase_usd_pairs()
    granularities = {"15m": 900, "1h": 3600, "4h": 14400}

    for pair in pairs:
        for name, interval in granularities.items():
            df = fetch_ohlcv(pair, interval)
            if len(df) < 200:
                continue
            signal = check_signal(df)
            if signal:
                msg = f"Signal for {pair} on {name}:
{signal}"
                bot.send_message(chat_id=CHAT_ID, text=msg)
            time.sleep(1)

if __name__ == "__main__":
    main()
