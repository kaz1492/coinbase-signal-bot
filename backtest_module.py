# backtest_module.py
# Backtesting engine to simulate signal performance historically

from utils import calculate_indicators
from lux_smc_engine import apply_smc_logic
import pandas as pd

def backtest(pair, historical_df):
    results = []
    df = calculate_indicators(historical_df.copy())
    for i in range(50, len(df)):
        sub_df = df.iloc[:i]
        smc_signal = apply_smc_logic(sub_df)
        if smc_signal:
            entry = smc_signal['entry']
            max_reached = sub_df['high'].iloc[-1]
            outcome = "hit_tp1" if max_reached >= smc_signal['targets'][0] else "failed"
            results.append({
                "index": i,
                "entry": entry,
                "outcome": outcome
            })
    return results
