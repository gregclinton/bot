from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import messages
import time
import asyncio

app = FastAPI()

# for now -- ultimately determined by the system
account = "TLG143623"
worker = "Hal"

@app.post('/messages')
async def post_message(req: Request):
    msg = await req.json()
    messages.post(account, worker, msg["body"])
    return "ok"

@app.get("/messages")
async def get_messages(after: float = 0):
    results = []
    start = time.time()

    while not results and time.time() - start < 60:
        for frm, body, timestamp in messages.chat(account, after):
            results.append({"from": frm, "body": body, "timestamp": timestamp})
        await asyncio.sleep(0.2)

    return results

app.mount("/", StaticFiles(directory = "chat", html = True))