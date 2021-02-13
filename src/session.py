import websocket
import threading
import json

class SessionError(BaseException):
    pass

class MonitorSession:
    def __init__(self, **kwargs):
        self.symbol = kwargs["symbol"]
        self.api_key = kwargs["api_key"]
        if "symbol_type" in kwargs:
            self.symbol_type = kwargs["symbol_type"]
        else:
            self.symbol_type = "stock"
        self.price = -1
        self._thread = threading.Thread(target=self.__create_session)
        self._thread.start()
        while self.price == -1:
            pass

    def __create_session(self):
        def on_message(ws, message):
            data = json.loads(message)
            if data["type"] == "error":
                raise SessionError(data["msg"])
            if data["type"] == "trade":
                self.price = data["data"][0]["p"]

        def on_error(ws, error):
            raise SessionError(f"Connection errored with '{error}'")

        def on_close(ws):
            raise SessionError("Connection closed")

        def on_open(ws):
            if self.symbol_type == "stock":
                ws.send(json.dumps({
                    "type": "subscribe",
                    "symbol": self.symbol
                }))
            elif self.symbol_type == "crypto":
                ws.send(json.dumps({
                    "type": "subscribe",
                    "symbol": f"BINANCE:{self.symbol.upper()}USDT"
                }))

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={self.api_key}",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_open = on_open)
        ws.run_forever()