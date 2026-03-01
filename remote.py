import requests
import os
import sys

pod_id = os.environ.get("POD_ID", "ABCD")
endpoint = f"https://{pod_id}-4000.proxy.runpod.net/messages"

def inbox(owner):
    for msg in requests.get(f"{endpoint}/{owner}").json():
        yield SimpleNamespace(**msg)

def post(frm, to, body):
    requests.post(endpoint, json = { "frm": frm, "to": to, "body": body })

if __name__ == "__main__":
    name = sys.argv[1]
    args = sys.argv[2:]
    {"post": post}[name](*args)