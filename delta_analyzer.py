def detect_delta_anomaly(df):
    delta = df['buy_volume'] - df['sell_volume']
    df['delta'] = delta
    signals = []
    for i in range(1, len(df)):
        if df['delta'][i] < 0 and df['close'][i] > df['open'][i]:
            signals.append('possible_sell_exhaustion')
        elif df['delta'][i] > 0 and df['close'][i] < df['open'][i]:
            signals.append('possible_buy_exhaustion')
        else:
            signals.append(None)
    df['delta_signal'] = signals
    return df