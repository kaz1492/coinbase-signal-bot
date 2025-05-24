# Handles scanning of all USD-quoted crypto pairs on Coinbase
import asyncio
from scanner import analyze_all_pairs

async def run_signal_scan(send_message):
    signals = analyze_all_pairs()

    if not signals:
        print("No signals were generated.")
        return

    for signal in signals:
        await send_message(signal)
