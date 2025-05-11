
import datetime

class DeltaAnalyzer:
    def __init__(self):
        self.order_data = []

    def process_trade(self, price, size, side, timestamp):
        self.order_data.append({
            "price": price,
            "size": size,
            "side": side,
            "timestamp": timestamp
        })

    def calculate_candle_delta(self, start_time, end_time):
        buy_volume = 0
        sell_volume = 0
        for trade in self.order_data:
            if start_time <= trade["timestamp"] <= end_time:
                if trade["side"] == "buy":
                    buy_volume += float(trade["size"])
                elif trade["side"] == "sell":
                    sell_volume += float(trade["size"])
        delta = buy_volume - sell_volume
        return delta, buy_volume, sell_volume
