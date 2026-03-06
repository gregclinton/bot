import requests
import os
import telegram

endpoint = os.environ.get("MESSAGES_URL")

def inbox(owner):
    if owner == "Hal":
        for msg in telegram.inbox():
            yield msg

    res = requests.get(f"{endpoint}/{owner}")
    if res.ok:
        try:
            for msg in res.json():
                yield msg
        except ValueError:
            pass

def post(frm, to, body):
    if to.startswith("CX1"):
        telegram.post(body)
    else:
        requests.post(endpoint, json = { "from": frm, "to": to, "body": body })