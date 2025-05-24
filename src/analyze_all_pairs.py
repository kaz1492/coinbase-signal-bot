
import pandas as pd
import numpy as np
from indicators import (
    calculate_sma, calculate_rsi,
    calculate_macd, calculate_bollinger_bands
)
from signal_logic import (
    is_crossing_up, rsi_oversold,
    macd_bullish, bollinger_breakout_up
)

def analyze_all_pairs():
    pairs = ["BTC/USD", "ETH/USD", "B3/USD", "NOT/USD"]
    timeframe = '1h'
    signals = []

    for pair in pairs:
        try:
            df = fetch_ohlcv(pair, timeframe)

            close = df['close']
            df['SMA20'] = calculate_sma(close, 20)
            df['SMA50'] = calculate_sma(close, 50)
            df['RSI'] = calculate_rsi(close)
            macd_line, signal_line, hist = calculate_macd(close)
            upper, mid, lower = calculate_bollinger_bands(close)

            conditions = [
                is_crossing_up(df['SMA20'], df['SMA50']),
                rsi_oversold(df['RSI']),
                macd_bullish(macd_line, signal_line),
                bollinger_breakout_up(close, upper)
            ]

            # اگر حداقل 3 شرط برقرار باشد، سیگنال صادر شود
            if sum(conditions) >= 3:
                signals.append(f"BUY signal for {pair} [{timeframe}]")

        except Exception as e:
            print(f"Error analyzing {pair}: {e}")

    return signals

def fetch_ohlcv(pair, tf):
    # داده‌ی تستی برای اجرای مستقل
    close = np.random.normal(100, 1, 100)
    df = pd.DataFrame({'close': close})
    return df
