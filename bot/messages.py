import requests
import os
import telegram

endpoint = os.environ.get("MESSAGES_URL")

def log(frm, to, body):
    print(f"From: {frm}\nTo: {to}\n{body}\n---------------------------\n", flush = True)

def inbox(owner):
    if owner == "Hal":
        for msg in telegram.inbox():
            frm = msg["from"]
            msg["from"] = f"CX1{frm}"
            log(msg["from"], msg["to"], msg["body"])
            yield msg

    res = requests.get(f"{endpoint}/{owner}")
    if res.ok:
        try:
            for msg in res.json():
                yield msg
        except ValueError:
            pass

def post(frm, to, body):
    log(frm, to, body)
    if to.startswith("CX1"):
        telegram.post(int(to[3:]), body)
    else:
        requests.post(endpoint, json = { "from": frm, "to": to, "body": body })