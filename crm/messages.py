import requests
import os
from types import SimpleNamespace

pod_id = os.environ.get("RUNPOD_POD_ID", "ABCD")
endpoint = f"https://{pod_id}-4000.proxy.runpod.net/messages"

def inbox(owner):
    res = requests.get(f"{endpoint}/{owner}")
    res.raise_for_status()
    for msg in res.json():
        yield SimpleNamespace(**msg)

def post(frm, to, body):
    requests.post(endpoint, json = { "frm": frm, "to": to, "body": body }).raise_for_status()