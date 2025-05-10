import pandas as pd

def calculate_indicators(data):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['rsi'] = calculate_rsi(df['close'])
    return df

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def generate_signal(df):
    if df['rsi'].iloc[-1] < 30 and df['close'].iloc[-1] > df['ma20'].iloc[-1]:
        return {
            'type': 'LONG',
            'entry': round(df['close'].iloc[-1], 4),
            'tp1': round(df['close'].iloc[-1] * 1.015, 4),
            'tp2': round(df['close'].iloc[-1] * 1.03, 4),
            'sl': round(df['close'].iloc[-1] * 0.975, 4)
        }
    return None