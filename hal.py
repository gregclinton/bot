import mail
import time

while True:
    msg = mail.get()
    if msg:
        print(msg)
    time.sleep(1)