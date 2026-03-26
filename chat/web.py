from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import messages
import time
import asyncio

app = FastAPI()

def get_account(token):
    # for now -- your system should implement
    return "TLG143623" if token else None

@app.post('/messages')
async def post_message(req: Request, token: str):
    msg = await req.json()
    account = get_account(token)
    if account:
        messages.post(account, "", msg["body"])
    return "ok"

@app.get("/messages")
async def get_messages(token: str, after: float = 0):
    posts = []
    start = time.time()

    account = get_account(token)
    if account:
        while not posts and time.time() - start < 60:
            for frm, body, timestamp in messages.chat(account, after):
                results.append({"from": frm, "body": body, "timestamp": timestamp})
            await asyncio.sleep(0.2)

    return {
        "token": "WEHTKWGTK", # for now -- your system should implement
        "posts": posts
    }

app.mount("/", StaticFiles(directory = "chat", html = True))