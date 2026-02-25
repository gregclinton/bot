import messages
import time

while True:
    msg = messages.get("/tmp/mail")
    if msg:
        print(msg)
    time.sleep(1)