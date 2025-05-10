import ccxt
from utils import calculate_indicators, generate_signal
from config import SYMBOLS
from telegram_sender import send_signal_message

# تعریف نگاشت تایم‌فریم‌های متنی به ثانیه برای Coinbase
GRANULARITY_MAP = {
    "15m": 900,
    "1h": 3600,
    "4h": 14400  # 4 ساعت = 4 * 3600 = 14400 ثانیه
}

def fetch_ohlcv(symbol, timeframe):
    exchange = ccxt.coinbase()
    granularity = GRANULARITY_MAP[timeframe]
    data = exchange.fetch_ohlcv(symbol, timeframe=granularity, limit=100)
    return data

def analyze_symbol(symbol, timeframe):
    try:
        raw_data = fetch_ohlcv(symbol, timeframe)
        df = calculate_indicators(raw_data)
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