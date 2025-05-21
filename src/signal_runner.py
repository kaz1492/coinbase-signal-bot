
from config import COINS, TIMEFRAMES
from coinbase_signal_bot import generate_signal
import data_loader  # فرض بر اینکه این ماژول موجود است و داده واقعی را می‌آورد

def run_all():
    for symbol in COINS:
        for tf in TIMEFRAMES:
            print(f"Fetching data for {symbol} [{tf}]...")
            try:
                df = data_loader.load(symbol, tf)
                if df is None or df.empty:
                    print(f"No data returned for {symbol} [{tf}]")
                    continue
                print(f"Running signal generation for {symbol} [{tf}]")
                signal = generate_signal(df, symbol, tf)
                if signal:
                    print(f"Signal sent for {symbol} [{tf}]")
                else:
                    print(f"No signal issued for {symbol} [{tf}]")
            except Exception as e:
                print(f"ERROR processing {symbol} [{tf}]:", e)

if __name__ == "__main__":
    run_all()
