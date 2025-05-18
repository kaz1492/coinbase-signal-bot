# coinbase_signal_bot.py
# Main logic for generating crypto trading signals using market data

from utils import calculate_indicators
from delta_analyzer import analyze_delta
from lux_smc_engine import apply_smc_logic
from telegram_sender import send_telegram_signal
from config import PAIRS, TIMEFRAMES

def generate_signals(market_data):
    signals = []
    for pair in PAIRS:
        for tf in TIMEFRAMES:
            df = market_data.get_price_data(pair, tf)
            df = calculate_indicators(df)
            smc_signal = apply_smc_logic(df)
            delta_info = analyze_delta(pair, tf)
            if smc_signal and delta_info['confirmation']:
                signal = {
                    "pair": pair,
                    "timeframe": tf,
                    "direction": smc_signal['direction'],
                    "entry": smc_signal['entry'],
                    "targets": smc_signal['targets'],
                    "stop_loss": smc_signal['stop_loss'],
                    "leverage": smc_signal['leverage'],
                    "win_rate": smc_signal['win_rate'],
                }
                signals.append(signal)
                send_telegram_signal(signal)
    return signals
from src.config import PAIRS, TIMEFRAMES, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
