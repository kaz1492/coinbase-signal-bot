import pandas as pd

def calculate_indicators(df):
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
    try:
        if df['rsi'].iloc[-1] < 30 and df['close'].iloc[-1] > df['ma20'].iloc[-1]:
            entry = round(df['close'].iloc[-1], 4)
            return {
                'type': 'LONG',
                'entry': entry,
                'tp1': round(entry * 1.015, 4),
                'tp2': round(entry * 1.03, 4),
                'tp3': round(entry * 1.05, 4),
                'tp4': round(entry * 1.08, 4),
                'sl': round(entry * 0.975, 4)
            }
    except Exception as e:
        print(f"Error in generate_signal: {str(e)}")
    return None