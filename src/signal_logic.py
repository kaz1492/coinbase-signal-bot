def is_crossing_up(short_ma, long_ma):
    return short_ma.iloc[-2] < long_ma.iloc[-2] and short_ma.iloc[-1] > long_ma.iloc[-1]

def is_crossing_down(short_ma, long_ma):
    return short_ma.iloc[-2] > long_ma.iloc[-2] and short_ma.iloc[-1] < long_ma.iloc[-1]

def rsi_overbought(rsi_series, threshold=70):
    return rsi_series.iloc[-1] > threshold and rsi_series.iloc[-2] <= threshold

def rsi_oversold(rsi_series, threshold=30):
    return rsi_series.iloc[-1] < threshold and rsi_series.iloc[-2] >= threshold

def macd_bullish(macd_line, signal_line):
    return macd_line.iloc[-2] < signal_line.iloc[-2] and macd_line.iloc[-1] > signal_line.iloc[-1]

def macd_bearish(macd_line, signal_line):
    return macd_line.iloc[-2] > signal_line.iloc[-2] and macd_line.iloc[-1] < signal_line.iloc[-1]

def bollinger_breakout_up(close, upper_band):
    return close.iloc[-2] <= upper_band.iloc[-2] and close.iloc[-1] > upper_band.iloc[-1]

def bollinger_breakout_down(close, lower_band):
    return close.iloc[-2] >= lower_band.iloc[-2] and close.iloc[-1] < lower_band.iloc[-1]
