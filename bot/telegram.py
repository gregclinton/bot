import requests
import os
from pathlib import Path

# https://t.me/Hal202020Bot
token = os.environ.get("TELEGRAM_TOKEN")
endpoint = f"https://api.telegram.org/bot{token}"
storage = Path("telegram")

chat_id = 0

def inbox():
    global chat_id

    offset = storage.read_text() if storage.exists() else 0

    res = requests.get(f"{endpoint}/getUpdates", params = { "offset": offset }).json()
    for update in res["result"]:
        storage.write_text(str( update["update_id"] + 1)) 
        message = update["message"]
        chat_id = message["chat"]["id"]
        frm = message["from"]["id"]
        body = message["text"]
        if body[0] != "/":
            yield {
                "from": f"CX1{frm}",
                "to": "Hal",
                "body": body,
                "timestamp": message["date"]
            }

def post(body):
    requests.post(f"{endpoint}/sendMessage", json = { "chat_id": chat_id, "text": body })
