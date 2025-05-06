
import pandas as pd

def fetch_ohlcv(pair, interval):
    # شبیه‌سازی داده‌های OHLCV برای تست (در عمل از API استفاده شود)
    return pd.DataFrame({
        "ma50": [1] * 200,
        "ma200": [1] * 200,
        "rsi": [30] * 200
    })

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
