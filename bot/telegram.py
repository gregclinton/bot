import requests
import os

# https://t.me/Hal202020Bot
token = os.environ.get("TELEGRAM_TOKEN")
endpoint = f"https://api.telegram.org/bot{token}"

updates = {
    "offset": 0
}

chat = {
    "id": 0
}

def inbox():
    global offset, chat_id

    res = requests.get(f"{endpoint}/getUpdates", params = { "offset": updates["offset"] }).json()
    for update in res["result"]:
        updates["offset"] = update["update_id"] + 1
        message = update["message"]
        chat["id"] = message["chat"]["id"]
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
    requests.post(f"{endpoint}/sendMessage", json = { "chat_id": chat["id"], "text": body })
