
from telegram_sender_updated import send_telegram_message

def generate_signal_message(pair: str, entry: float, signal_type: str = "long", margin_mode: str = "Isolated"):
    tp_percents = [0.015, 0.03, 0.05, 0.08]
    sl_percent = 0.025

    if signal_type.lower() == "long":
        tps = [entry * (1 + p) for p in tp_percents]
        sl = entry * (1 - sl_percent)
    else:
        tps = [entry * (1 - p) for p in tp_percents]
        sl = entry * (1 + sl_percent)

    volatility = tp_percents[-1] + sl_percent
    if volatility < 0.05:
        leverage = "x3"
    elif volatility < 0.08:
        leverage = "x5"
    elif volatility < 0.12:
        leverage = "x10"
    else:
        leverage = "x20"

    direction = "خرید" if signal_type.lower() == "long" else "فروش"
    message = f"{pair} – سیگنال {direction} (فیوچرز)\n\n"
    message += f"ورود: {entry:.4f}\nاهرم: {leverage} – {margin_mode}\nتایم‌فریم: 15m\n\n🎯 تارگت‌ها:"
    for i, tp in enumerate(tps, 1):
        percent = tp_percents[i - 1] * 100
        message += f"\n• TP{i}: {tp:.4f} ({'+' if signal_type=='long' else '-'}{percent:.1f}%)"
    message += f"\n\n❌ استاپ لاس: {sl:.4f} ({'-' if signal_type=='long' else '+'}{sl_percent * 100:.1f}%)"
    message += "\n\nتحلیل: سیگنال مبتنی بر دلتا، حجم و ساختار RTM"
    return message

# Example: always check B3USD
pair = "B3USD"
entry_price = 0.0184
signal_type = "long"

msg = generate_signal_message(pair, entry_price, signal_type)
print(msg)
send_telegram_message(msg)
