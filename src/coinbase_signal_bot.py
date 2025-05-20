
import pandas as pd
from signal_generator import generate_signals
from telegram_sender import send_signal_to_telegram
from config import PAIRS, TIMEFRAMES

def run_bot():
    for pair in PAIRS:
        for tf in TIMEFRAMES:
            try:
                print(f"Processing {pair} on {tf} timeframe...")
                df = pd.read_csv(f"data/{pair.replace('/', '-')}_{tf}.csv")
                signal = generate_signals(df, pair, tf)
                if signal:
                    send_signal_to_telegram(signal)
            except Exception as e:
                print(f"Error processing {pair} [{tf}]: {e}")

if __name__ == "__main__":
    run_bot()
