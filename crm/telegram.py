import requests
import os
import time

# https://t.me/Hal202020Bot
token = os.environ.get("TELEGRAM_TOKEN")
endpoint = f"https://api.telegram.org/bot{token}"
offset = 0

while True:
    res = requests.get(f"{endpoint}/getUpdates", params = { "offset": offset }).json()
    for update in res["result"]:
        offset = update["update_id"] + 1
        message = update["message"]
        print(message["text"])
        requests.post(f"{endpoint}/sendMessage", json = { "chat_id": message["chat"]["id"], "text": "hello" })
    time.sleep(1)

