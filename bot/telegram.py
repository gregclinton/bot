import requests
import os
from pathlib import Path
import json

# https://t.me/Hal202020Bot
token = os.environ.get("TELEGRAM_TOKEN")
endpoint = f"https://api.telegram.org/bot{token}"
storage = Path("telegram")
cursor = json.loads(storage.read_text()) if storage.exists() else { "offset": 0 }
chat_id = 0

def inbox():
    global chat_id
    msgs = []

    res = requests.get(f"{endpoint}/getUpdates", params = { "offset": cursor["offset"] }).json()
    for update in res["result"]:
        cursor["offset"] = update["update_id"] + 1
        message = update["message"]
        chat_id = message["chat"]["id"]
        frm = message["from"]["id"]
        body = message["text"]
        if body[0] != "/":
            msgs.append({
                "from": f"CX1{frm}",
                "to": "Hal",
                "body": body,
                "timestamp": message["date"]
            })

    storage.write_text(json.dumps(cursor))
    return msgs


def post(body):
    requests.post(f"{endpoint}/sendMessage", json = { "chat_id": chat_id, "text": body })
