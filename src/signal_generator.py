
import pandas as pd

def generate_signals(df, pair, timeframe):
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['RSI'] = calculate_rsi(df['close'])

    last_rsi = df['RSI'].iloc[-1]
    current_price = df['close'].iloc[-1]

    if last_rsi < 30:
        return {
            'pair': pair,
            'timeframe': timeframe,
            'type': 'Buy',
            'entry': current_price,
            'tp1': current_price * 1.05,
            'tp2': current_price * 1.10,
            'tp3': current_price * 1.20,
            'tp4': current_price * 1.35,
            'sl': current_price * 0.95,
            'leverage': '10x'
        }
    elif last_rsi > 70:
        return {
            'pair': pair,
            'timeframe': timeframe,
            'type': 'Sell',
            'entry': current_price,
            'tp1': current_price * 0.95,
            'tp2': current_price * 0.90,
            'tp3': current_price * 0.85,
            'tp4': current_price * 0.80,
            'sl': current_price * 1.05,
            'leverage': '10x'
        }
    else:
        return None

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
