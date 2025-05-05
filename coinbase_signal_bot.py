
import pandas as pd
import requests
import time
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

telegram_token = "8042153193:AAHwBA7Wgkhe9eU26eX9hfqPA-uch0gE2fE"
chat_id = "99455629"
timeframes = {"15m": 15, "1h": 60, "4h": 240}

def get_coinbase_usd_pairs():
    url = "https://api.exchange.coinbase.com/products"
    response = requests.get(url)
    data = response.json()
    usd_pairs = [item['id'] for item in data if item['quote_currency'] == 'USD' and item['trading_disabled'] is False]
    return usd_pairs

def get_ohlc(pair, granularity):
    url = f"https://api.exchange.coinbase.com/products/{pair}/candles?granularity={granularity*60}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = pd.DataFrame(response.json(), columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.sort_values('time', inplace=True)
    return data

def compute_signals(df):
    df['ma50'] = df['close'].rolling(window=50).mean()
    df['ma200'] = df['close'].rolling(window=200).mean()
    df['rsi'] = ta_rsi(df['close'], 14)

    ma_cross_long = df['ma50'].iloc[-1] > df['ma200'].iloc[-1] and df['ma50'].iloc[-2] < df['ma200'].iloc[-2]
    ma_cross_short = df['ma50'].iloc[-1] < df['ma200'].iloc[-1] and df['ma50'].iloc[-2] > df['ma200'].iloc[-2]
    rsi_long = df['rsi'].iloc[-1] < 30
    rsi_short = df['rsi'].iloc[-1] > 70

    high20 = df['high'].iloc[-21:-1].max()
    low20 = df['low'].iloc[-21:-1].min()
    bos_long = df['high'].iloc[-1] > high20
    bos_short = df['low'].iloc[-1] < low20

    fvg_up = df['low'].iloc[-3] > df['high'].iloc[-1]
    fvg_down = df['high'].iloc[-3] < df['low'].iloc[-1]

    long_signal = ma_cross_long and rsi_long and bos_long and fvg_up
    short_signal = ma_cross_short and rsi_short and bos_short and fvg_down

    return long_signal, short_signal, df['close'].iloc[-1]

def ta_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

usd_pairs = get_coinbase_usd_pairs()
usd_pairs = usd_pairs[:20]

for pair in usd_pairs:
    for tf_label, tf_minutes in timeframes.items():
        df = get_ohlc(pair, tf_minutes)
        if df is None or len(df) < 201:
            continue
        long_signal, short_signal, price = compute_signals(df)
        if long_signal or short_signal:
            signal_type = "LONG" if long_signal else "SHORT"
            msg = f"Signal Alert!\nPair: {pair}\nTimeframe: {tf_label}\nType: {signal_type}\nPrice: {price:.5f}\nConditions Met: MA+RSI+FVG+BOS"
            send_telegram_message(msg)
            print(msg)
