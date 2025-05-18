# signal_runner.py
# Orchestrates the signal generation loop and manages execution flow

from coinbase_signal_bot import generate_signals
from data_collector import get_market_data
from time import sleep

INTERVAL_SECONDS = 60  # Adjust as needed

def run_signal_bot():
    while True:
        try:
            market_data = get_market_data()
            signals = generate_signals(market_data)
            print(f"{len(signals)} signals generated.")
        except Exception as e:
            print(f"Error during signal run: {e}")
        sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run_signal_bot()
