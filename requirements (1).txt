
# Coinbase Signal Bot

This bot scans USD trading pairs on Coinbase across 15m, 1h, and 4h timeframes.
It checks for:
- MA50/MA200 crossover
- RSI oversold/overbought
- FVG (Fair Value Gap) presence
- BOS (Break of Structure) confirmation

## How to Run
1. Make sure Python 3 is installed.
2. Install required libraries:
   pip install pandas requests
3. Run the bot:
   python coinbase_signal_bot.py
