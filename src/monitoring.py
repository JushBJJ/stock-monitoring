from session import MonitorSession
import time

s = MonitorSession("BTC")
s.wait_until_ready()
while True:
    print("Current bitcoin price: " + str(s.price))
    time.sleep(1)