
os.getenv("TELEGRAM_CHAT_ID")


async def send_signal(symbol, entry_price, signal_type, score):
    tp_factors = [1.05, 1.10, 1.20, 1.30] if signal_type == "LONG" else [0.95, 0.90, 0.85, 0.80]
    sl_factor = 0.975 if signal_type == "LONG" else 1.025

    targets = [round(entry_price * f, 6) for f in tp_factors]
    sl = round(entry_price * sl_factor, 6)

    msg = f"{signal_type} SIGNAL - {symbol}\n"
    msg += f"Entry Price: {entry_price}\n"
    msg += "Targets:\n"
    msg += f"• TP1: {targets[0]}\n"
    msg += f"• TP2: {targets[1]}\n"
    msg += f"• TP3: {targets[2]}\n"
    msg += f"• TP4: {targets[3]}\n"
    msg += f"Stop Loss: {sl}\n"
    msg += f"Confidence Score: {score}/5"

    await bot.send_message(chat_id=CHAT_ID, text=msg)

# For test purposes
if __name__ == "__main__":
    asyncio.run(send_signal("BTC/USD", 27000, "LONG", 4.5))
