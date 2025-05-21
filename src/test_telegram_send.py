
from telegram_sender import send_to_telegram

# ساخت سیگنال تستی
signal = {
    "type": "TEST",
    "symbol": "B3-USD",
    "timeframe": "15m",
    "price": 0.0183,
    "delta_divergence": "Positive Divergence",
    "smc_pattern": "FVG Detected"
}

send_to_telegram(signal)
