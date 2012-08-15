from websocket import create_connection
import thread
import time

ws = create_connection("ws://localhost:8000")
ws.settimeout(800)
while True:
    ws.send("HELLO")
    time.sleep(5)