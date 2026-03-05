import requests
import os
from types import SimpleNamespace

endpoint = os.environ.get("MESSAGES_URL")

def inbox(owner):
    res = requests.get(f"{endpoint}/{owner}")
    for msg in res.json():
        yield SimpleNamespace(**msg)

def post(frm, to, body):
    requests.post(f"{endpoint}/{to}", json = { "frm": frm, "body": body })