import pandas as pd

def detect_structure(df):
    df['bos'] = df['high'] > df['high'].shift(1)
    df['choch'] = df['low'] < df['low'].shift(1)
    return df

def detect_order_blocks(df):
    df['order_block'] = (df['open'] < df['close']) & (df['volume'] > df['volume'].rolling(5).mean())
    return df

def detect_premium_discount_zone(df):
    high = df['high'].rolling(window=20).max()
    low = df['low'].rolling(window=20).min()
    df['mid'] = (high + low) / 2
    df['zone'] = df['close'] > df['mid']
    return df

def analyze_lux_smc(df):
    df = detect_structure(df)
    df = detect_order_blocks(df)
    df = detect_premium_discount_zone(df)
    return df