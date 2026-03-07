import requests
import os
from pathlib import Path
import json

# https://t.me/Hal202020Bot
token = os.environ.get("TELEGRAM_TOKEN")
endpoint = f"https://api.telegram.org/bot{token}"
storage = Path("telegram")

def inbox():
    offset = int(storage.read_text()) if storage.exists() else 0

    print("request")
    res = requests.get(f"{endpoint}/getUpdates", params = { "timeout": 50, "offset": offset }).json()
    for update in res["result"]:
        offset = update["update_id"] + 1
        message = update["message"]
        frm = message["from"]["id"]
        body = message["text"]
        if body[0] != "/":
            yield {
                "from": frm,
                "to": "Hal",
                "body": body,
                "timestamp": int(message["date"])
            }

    storage.write_text(str(offset))


def post(to, body):
    # except for group chats, chat id is same as user id
    requests.post(f"{endpoint}/sendMessage", json = { "chat_id": to, "text": body })
