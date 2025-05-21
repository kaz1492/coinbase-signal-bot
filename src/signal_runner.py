
from config import COINS, TIMEFRAMES
from coinbase_signal_bot import generate_signal
import data_loader  # hypothetical module to get data

def run_all():
    for symbol in COINS:
        for tf in TIMEFRAMES:
            df = data_loader.load(symbol, tf)
            if df is not None:
                try:
                    generate_signal(df, symbol, tf)
                except Exception as e:
                    print(f"Error processing {symbol} [{tf}]:", e)
