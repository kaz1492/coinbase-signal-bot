import ccxt
from utils import calculate_indicators, generate_signal
from config import TIMEFRAMES, SYMBOLS
from telegram_sender import send_signal_message

def fetch_ohlcv(symbol, timeframe, limit=100):
    exchange = ccxt.coinbase()
    data = exchange.fetch_ohlcv(symbol, timeframe, limit)
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
    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            analyze_symbol(symbol, tf)

if __name__ == "__main__":
    run()