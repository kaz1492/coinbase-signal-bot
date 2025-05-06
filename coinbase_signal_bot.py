import os
import requests
import asyncio
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

def get_usd_pairs():
    url = "https://api.exchange.coinbase.com/products"
    response = requests.get(url)
    data = response.json()
    return [p["id"] for p in data if p["quote_currency"] == "USD"]

def get_latest_price(product_id):
    url = f"https://api.exchange.coinbase.com/products/{product_id}/ticker"
    response = requests.get(url)
    if response.status_code == 200:
        return float(response.json()["price"])
    return None

async def send_signal(symbol, entry_price, signal_type="خرید"):
    tp1 = round(entry_price * 1.015, 4)
    tp2 = round(entry_price * 1.03, 4)
    tp3 = round(entry_price * 1.05, 4)
    tp4 = round(entry_price * 1.08, 4)
    sl = round(entry_price * 0.975, 4)

    message = (
        f"📢 سیگنال {signal_type.upper()} - {symbol}\n"
        f"✅ ورود: {entry_price}\n"
        f"🎯 تارگت‌ها:\n"
        f"• TP1: {tp1}\n"
        f"• TP2: {tp2}\n"
        f"• TP3: {tp3}\n"
        f"• TP4: {tp4}\n"
        f"❌ استاپ لاس: {sl}"
    )

    await bot.send_message(chat_id=CHAT_ID, text=message)

async def main():
    usd_pairs = get_usd_pairs()
    print(f"Checking {len(usd_pairs)} USD pairs...")
    for pair in usd_pairs:
        price = get_latest_price(pair)
        if price and price > 0:
            await send_signal(pair, price)
            await asyncio.sleep(1)  # برای جلوگیری از spam تلگرام

if __name__ == "__main__":
    asyncio.run(main())