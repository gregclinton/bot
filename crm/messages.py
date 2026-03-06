import requests
import os

endpoint = os.environ.get("MESSAGES_URL")

def inbox(owner):
    r = requests.get(f"{endpoint}/{owner}")
    if r.ok:
        try:
            for msg in r.json():
                yield msg
        except ValueError:
            print("ouch")
            pass

def post(frm, to, body):
    requests.post(endpoint, json = { "from": frm, "to": to, "body": body })