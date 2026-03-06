import requests
import os

# https://t.me/Hal202020Bot
token = os.environ.get("TELEGRAM_TOKEN")
endpoint = f"https://api.telegram.org/bot{token}"
offset = 0
chat_id = 0

def inbox():
    res = requests.get(f"{endpoint}/getUpdates", params = { "offset": offset }).json()
    for update in res["result"]:
        offset = update["update_id"] + 1
        message = update["message"]
        chat_id = message["chat"]["id"]
        yield 

def post(to, body):
    requests.post(f"{endpoint}/sendMessage", json = { "chat_id": chat_id, "text": body })
