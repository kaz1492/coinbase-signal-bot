# Handles scanning of all USD-quoted pairs for signal generation
import asyncio
from scanner import analyze_all_pairs

async def run_signal_scan(send_message):
    signals = analyze_all_pairs()
    for signal in signals:
        await send_message(signal)
if not signal:
    print(f"No signal for {symbol} due to indicator mismatch.")
