def calculate_rsi(df, period=14):
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def check_signal(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    signal = ""
    if prev["ma50"] < prev["ma200"] and last["ma50"] > last["ma200"]:
        signal += "Golden Cross | "
    if last["rsi"] < 30:
        signal += "RSI Oversold | "
    if last["rsi"] > 70:
        signal += "RSI Overbought | "
    return signal.strip(" | ")