from session import MonitorSession, SessionError
import time

API_KEY = "c0jsoj748v6qqehfm3qg"

try:
    s = MonitorSession(symbol="BTC", api_key=API_KEY, symbol_type="crypto")
except SessionError:
    print("exit/")

while True:
    try:
        print("Current bitcoin price: " + str(s.price))
        time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down session.")
        s.shutdown()
        break
