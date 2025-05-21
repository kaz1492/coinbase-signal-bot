
import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.exchange.coinbase.com"

def load(symbol, timeframe):
    # Map timeframe to Coinbase granularity (in seconds)
    tf_map = {
        "15m": 900,
        "1h": 3600,
        "4h": 21600  # use 6h granularity instead of unsupported 4h (14400)
    }
    granularity = tf_map.get(timeframe)
    if granularity is None:
        print(f"Unsupported timeframe: {timeframe}")
        return None

    try:
        url = f"{BASE_URL}/products/{symbol}/candles?granularity={granularity}"
        response = requests.get(url)
        response.raise_for_status()
        candles = response.json()

        # Coinbase returns: [ time, low, high, open, close, volume ]
        df = pd.DataFrame(candles, columns=[
            "timestamp", "low", "high", "open", "close", "volume"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df.sort_values("timestamp", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol} [{timeframe}]:", e)
        return None
