
import requests

def send_telegram_signal(signal):
    TOKEN = "8042153193:AAHykVSyPK2gUGTYh3hv-BM77tuFglWEpek"
    CHAT_ID = "99455629"

    message = f"**Test Signal**\n" \
              f"Type: {signal['type']}\n" \
              f"Symbol: {signal['symbol']}\n" \
              f"Entry: {signal['entry']}\n" \
              f"Target1: {signal['target1']}\n" \
              f"Stoploss: {signal['stoploss']}\n" \
              f"Leverage: {signal['leverage']}x"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=data)
    print(f"Telegram response: {response.status_code}, {response.text}")
