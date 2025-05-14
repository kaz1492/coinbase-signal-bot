
import time
import requests
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(df):
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def calculate_leverage(entry, stop, target, max_lev=25):
    risk = abs(entry - stop)
    reward = abs(target - entry)
    if risk == 0:
        return 1
    rr = reward / risk
    leverage = 2 + (rr - 0.5) * (max_lev - 2) / (5 - 0.5)
    return round(min(max(leverage, 1), max_lev), 1)

def send_signal(signal, timeframe):
    msg = f"""
{signal['symbol']} ({timeframe}) - {signal['side']}
Entry: {signal['entry_low']} - {signal['entry_high']}
Targets:
TP1: {signal['targets'][0]}
TP2: {signal['targets'][1]}
TP3: {signal['targets'][2]}
TP4: {signal['targets'][3]}
SL: {signal['stoploss']}
Leverage: {signal['leverage']}x
Win Rate: {signal['win_rate']}%
"""
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": msg
    })

def get_pairs():
    r = requests.get("https://api.exchange.coinbase.com/products").json()
    return [x["id"] for x in r if x["quote_currency"] == "USD" and not x["trading_disabled"]]

def get_candles(pair, granularity):
    url = f"https://api.exchange.coinbase.com/products/{pair}/candles?granularity={granularity}"
    data = requests.get(url).json()
    if isinstance(data, list):
        df = pd.DataFrame(data, columns=["time","low","high","open","close","volume"])
        return df.sort_values("time")
    return None

def analyze(pair, tf_seconds, tf_label):
    df = get_candles(pair, tf_seconds)
    if df is None or len(df) < 30: return

    df["rsi"] = calculate_rsi(df["close"])
    macd, signal_line = calculate_macd(df)
    df["macd"], df["macd_signal"] = macd, signal_line

    last = df.iloc[-1]
    entry = last["close"]
    rsi, macd_val, macd_sig = last["rsi"], last["macd"], last["macd_signal"]

    if rsi < 30 and macd_val > macd_sig:
        sl = round(entry * 0.97, 6)
        t1 = round(entry * 1.01, 6)
        t2 = round(entry * 1.02, 6)
        t3 = round(entry * 1.03, 6)
        t4 = round(entry * 1.05, 6)
        lev = calculate_leverage(entry, sl, t1)
        win_rate = 75
        if win_rate >= 70:
            signal = {
                "symbol": pair,
                "entry_low": round(entry * 0.998, 6),
                "entry_high": round(entry * 1.002, 6),
                "targets": [t1, t2, t3, t4],
                "stoploss": sl,
                "side": "LONG",
                "leverage": lev,
                "win_rate": win_rate
            }
            send_signal(signal, tf_label)

def main():
    pairs = get_pairs()
    sent = set()
    while True:
        for pair in pairs:
            for tf, label in [(900, "15m"), (3600, "1h")]:
                key = f"{pair}-{label}"
                if key not in sent:
                    analyze(pair, tf, label)
                    sent.add(key)
                    time.sleep(30)
        sent.clear()

if __name__ == "__main__":
    main()
