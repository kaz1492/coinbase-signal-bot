
import requests
import pandas as pd

def fetch_ohlcv(pair, interval):
    url = f"https://api.exchange.coinbase.com/products/{pair}/candles?granularity={interval}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
    df = df.sort_values("time")
    df["ma50"] = df["close"].rolling(window=50).mean()
    df["ma200"] = df["close"].rolling(window=200).mean()
    df["rsi"] = calculate_rsi(df["close"], 14)
    return df

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0.0).rolling(window=period).mean()
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
