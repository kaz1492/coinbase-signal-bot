import ccxt
import pandas as pd
from utils import calculate_indicators, generate_signal
from config import SYMBOLS
from telegram_sender import send_signal_message

GRANULARITY_MAP = {
    "15m": 900,
    "1h": 3600,
    "4h": 14400
}

def fetch_ohlcv(symbol, timeframe):
    exchange = ccxt.coinbase()
    granularity = GRANULARITY_MAP[timeframe]
    data = exchange.fetch_ohlcv(symbol, timeframe=granularity, limit=100)
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def analyze_symbol(symbol, timeframe):
    try:
        df = fetch_ohlcv(symbol, timeframe)
        df = calculate_indicators(df)
        signal = generate_signal(df)
        if signal:
            send_signal_message(symbol, signal, timeframe)
    except Exception as e:
        print(f"Error processing {symbol} [{timeframe}]: {str(e)}")

def run():
    timeframes = ["15m", "1h", "4h"]
    for symbol in SYMBOLS:
        for tf in timeframes:
            analyze_symbol(symbol, tf)

if __name__ == "__main__":
    run()