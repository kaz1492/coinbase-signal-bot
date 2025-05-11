import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import websocket
import json
import threading
import logging
import time
from datetime import datetime
from src.analysis.delta_analyzer import DeltaAnalyzer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CoinbaseWebSocket:
    def __init__(self, product_ids=["FIL-USD", "BTC-USD", "ETH-USD"]):
        self.ws = None
        self.product_ids = product_ids
        self.delta_analyzer = DeltaAnalyzer()
        self.reconnect_attempts = 0
        self.max_reconnects = 5

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if data.get("type") == "match" and data.get("product_id") in self.product_ids:
                price = float(data["price"])
                size = float(data["size"])
                side = data["side"]
                timestamp = datetime.strptime(data["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                self.delta_analyzer.process_trade(price, size, side, timestamp)
        except Exception as e:
            logging.error(f"Error in on_message: {e}")

    def on_error(self, ws, error):
        logging.error(f"WebSocket error: {error}")
        self.reconnect()

    def on_close(self, ws, close_status_code, close_msg):
        logging.warning(f"WebSocket closed: {close_status_code} - {close_msg}")
        self.reconnect()

    def reconnect(self):
        if self.reconnect_attempts < self.max_reconnects:
            self.reconnect_attempts += 1
            logging.info(f"Reconnecting... Attempt {self.reconnect_attempts}")
            time.sleep(5)
            self.run()
        else:
            logging.error("Max reconnect attempts reached.")
            from src.notification.telegram_sender import send_telegram_message
            send_telegram_message("خطا: اتصال WebSocket قطع شد!")

    def on_open(self, ws):
        self.reconnect_attempts = 0
        sub_msg = {
            "type": "subscribe",
            "channels": [{"name": "matches", "product_ids": self.product_ids}]
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
