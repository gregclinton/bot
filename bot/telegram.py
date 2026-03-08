# while true; do python3 telegram.py; done

import requests
import os
import sys

# https://t.me/Hal202020Bot
token = os.environ.get("TELEGRAM_TOKEN")

if not token:
    print("TELEGRAM_TOKEN not set.", flush = True)
    sys.exit()

endpoint = f"https://api.telegram.org/bot{token}"

def post(to, body):
    # except for group chats, chat id is same as user id
    requests.post(f"{endpoint}/sendMessage", json = { "chat_id": to, "text": body })

if __name__ == "__main__":
    import messages

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