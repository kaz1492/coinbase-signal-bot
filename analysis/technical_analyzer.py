import talib
import numpy as np
from delta_analyzer import DeltaAnalyzer

class TechnicalAnalyzer:
    def __init__(self):
        self.delta_analyzer = DeltaAnalyzer()

    def analyze(self, trades, start_time, end_time):
        delta, buy_vol, sell_vol = self.delta_analyzer.calculate_candle_delta(start_time, end_time)
        prices = np.array([t['price'] for t in trades if start_time <= t['timestamp'] <= end_time])
        if len(prices) < 14:
            return {"signal": None, "rsi": 50, "delta": delta, "buy_volume": buy_vol, "sell_volume": sell_vol, "atr": 0.02}
        
        rsi = talib.RSI(prices, timeperiod=14)[-1]
        macd, signal, _ = talib.MACD(prices)[-1] if len(prices) >= 26 else (0, 0, 0)
        atr = talib.ATR(prices, prices, prices, timeperiod=14)[-1] if len(prices) >= 14 else 0.02
        
        signal_type = None
        if rsi < 30 and delta < 0 and buy_vol > sell_vol * 1.2 and macd > signal:
            signal_type = "long"
        elif rsi > 70 and delta > 0 and sell_vol > buy_vol * 1.2 and macd < signal:
            signal_type = "short"
            
        return {
            "signal": signal_type,
            "rsi": rsi,
            "delta": delta,
            "buy_volume": buy_vol,
            "sell_volume": sell_vol,
            "atr": atr
        }