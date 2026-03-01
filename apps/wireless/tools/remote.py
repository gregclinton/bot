import requests
import os

pod_id = os.environ.get("POD_ID", "ABCD")
messages_endpoint = f"https://{pod_id}-4000.proxy.runpod.net/messages"

def inbox(owner):
    for msg in requests.get(f"{messages_endpoint}/{owner}").json():
        yield SimpleNamespace(**msg)

def post(frm, to, body):
    requests.post(messages_endpoint, json = { "frm": frm, "to": to, "body": body })