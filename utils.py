import requests
import pandas as pd

def get_coinbase_usd_pairs():
    url = "https://api.exchange.coinbase.com/products"
    data = requests.get(url).json()
    return [item['id'] for item in data if item['quote_currency'] == 'USD']

def fetch_ohlcv(pair, interval_seconds):
    url = f"https://api.exchange.coinbase.com/products/{pair}/candles?granularity={interval_seconds}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df.sort_values("time")
    df["ma50"] = df["close"].rolling(50).mean()
    df["ma200"] = df["close"].rolling(200).mean()
    return df