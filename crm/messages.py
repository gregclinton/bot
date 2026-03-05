import requests
import os

endpoint = os.environ.get("MESSAGES_URL")

def inbox(owner):
    for msg in requests.get(f"{endpoint}/{owner}").json():
        yield msg

def post(frm, to, body):
    requests.post(endpoint, json = { "from": frm, "to": to, "body": body })