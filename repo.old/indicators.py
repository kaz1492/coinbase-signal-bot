import pandas as pd
import numpy as np
import ta

def calculate_indicators(df):
    df = df.copy()
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()
    df["ema20"] = ta.trend.EMAIndicator(close=df["close"], window=20).ema_indicator()
    df["ema50"] = ta.trend.EMAIndicator(close=df["close"], window=50).ema_indicator()
    macd = ta.trend.MACD(close=df["close"])
    df["macd_diff"] = macd.macd_diff()
    df["adx"] = ta.trend.ADXIndicator(high=df["high"], low=df["low"], close=df["close"]).adx()
    df["atr"] = ta.volatility.AverageTrueRange(high=df["high"], low=df["low"], close=df["close"]).average_true_range()
    return df

def detect_candle_patterns(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    pattern = None

    # Bullish Engulfing
    if prev["close"] < prev["open"] and last["close"] > last["open"] and last["close"] > prev["open"] and last["open"] < prev["close"]:
        pattern = "bullish_engulfing"
    # Bearish Engulfing
    elif prev["close"] > prev["open"] and last["close"] < last["open"] and last["open"] > prev["close"] and last["close"] < prev["open"]:
        pattern = "bearish_engulfing"

    return pattern

def score_signal(row, pattern, signal_type):
    score = 0
    if signal_type == "LONG":
        if row["rsi"] < 35: score += 1
        if row["ema20"] > row["ema50"]: score += 1
        if row["macd_diff"] > 0: score += 1
        if row["adx"] > 20: score += 1
        if pattern == "bullish_engulfing": score += 1
    elif signal_type == "SHORT":
        if row["rsi"] > 65: score += 1
        if row["ema20"] < row["ema50"]: score += 1
        if row["macd_diff"] < 0: score += 1
        if row["adx"] > 20: score += 1
        if pattern == "bearish_engulfing": score += 1
    return score