
import websocket
import json
import threading
from datetime import datetime, timedelta
from delta_analyzer import DeltaAnalyzer

class CoinbaseWebSocket:
    def __init__(self, product_id="FIL-USD"):
        self.ws = None
        self.product_id = product_id
        self.delta_analyzer = DeltaAnalyzer()

    def on_message(self, ws, message):
        data = json.loads(message)
        if data.get("type") == "match" and data.get("product_id") == self.product_id:
            price = float(data["price"])
            size = float(data["size"])
            side = data["side"]
            timestamp = datetime.strptime(data["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            self.delta_analyzer.process_trade(price, size, side, timestamp)

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed.")

    def on_open(self, ws):
        sub_msg = {
            "type": "subscribe",
            "channels": [{"name": "matches", "product_ids": [self.product_id]}]
        }
        ws.send(json.dumps(sub_msg))

    def run(self):
        ws_url = "wss://ws-feed.exchange.coinbase.com"
        self.ws = websocket.WebSocketApp(ws_url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open)
        thread = threading.Thread(target=self.ws.run_forever)
        thread.start()

    def get_latest_delta_signal(self):
        now = datetime.utcnow()
        start = now - timedelta(minutes=15)
        delta, buy, sell = self.delta_analyzer.calculate_candle_delta(start, now)
        if delta < 0 and buy > 0:
            return f"احتمال برگشت قیمت! دلتا منفی ولی خریداران فعالند.
دلتا: {delta:.2f} | خرید: {buy:.2f} | فروش: {sell:.2f}"
        return None
