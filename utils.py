# utils.py
# Contains helper functions for calculating technical indicators

import pandas as pd

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ma(series, window):
    return series.rolling(window=window).mean()

def calculate_indicators(df):
    df['rsi'] = calculate_rsi(df['close'])
    df['ma20'] = calculate_ma(df['close'], 20)
    df['ma50'] = calculate_ma(df['close'], 50)
    return df
