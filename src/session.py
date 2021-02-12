import websocket
import threading
import json

class SessionError(BaseException):
    pass

class MonitorSession:
    def __init__(self, symbol="BTC"):
        self.symbol = symbol
        self._full_symbol = symbol + "USDT"
        self.price = -1
        self._thread = threading.Thread(target=self.__create_session)
        self._thread.start()

    def wait_until_ready(self):
        while self.price == -1:
            pass

    def __create_session(self):
        def on_message(ws, message):
            message = json.loads(message)
            if "p" in message and "s" in message:
                self.price = float(message["p"])

        def on_error(ws, error):
            raise SessionError(f"Connection errored with '{error}'")

        def on_close(ws):
            raise SessionError("Connection closed")

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(f"wss://stream.binance.com:9443/ws/{self.symbol.lower()}usdt@aggTrade",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
        ws.run_forever()