import requests
import os

endpoint = os.environ.get("MESSAGES_URL")

def inbox(owner):
    res = requests.get(f"{endpoint}/{owner}")
    if res.ok:
        try:
            for msg in res.json():
                yield msg
        except ValueError:
            pass

def post(frm, to, body):
    requests.post(endpoint, json = { "from": frm, "to": to, "body": body })