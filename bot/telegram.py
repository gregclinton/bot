import requests
import os
import sys
from time import sleep
import messages

token = os.environ.get("TELEGRAM_TOKEN")

if not token:
    print("TELEGRAM_TOKEN not set.", flush = True)
    sleep(2)
    sys.exit()

endpoint = f"https://api.telegram.org/bot{token}"

def post(to, body):
    # except for group chats, chat id is same as ody)
    requests.post(f"{endpoint}/sendMessage", json = { "chat_id": to, "text": body })

def updates():
    offset = int(open("offset").read()) if os.path.exists("offset") else 0
    res = requests.get(f"{endpoint}/getUpdates", params = { "timeout": 30, "offset": offset })
    res.raise_for_status()
    res = res.json()
    for update in res["result"]:
        offset = update["update_id"]
        message = update["message"]
        frm = message["from"]["id"]
        body = message["text"]
        messages.post(f"TLG{frm}", "Hal", body)
        open("offset","w").write(str(offset + 1))

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])