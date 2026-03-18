from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import messages
from worker import chat
import time
import asyncio

app = FastAPI()

@app.post('/messages')
async def post_message(req: Request):
    msg = await req.json()
    messages.post(msg["from"], msg["to"], msg["body"])
    return "ok"

@app.get("/messages/{worker}/{account}")
async def get_messages(worker: str, account: str, start: int = 0, timeout: int = 10):
    results = []
    start = time.time()

    while True:
        for order, frm, body in chat(worker, account, start:
            results.append({"order": order, "from": frm, "body": body})
        if results or time.time() - start > timeout:
            break
        await asyncio.sleep(0.2)

    return results

app.mount("/", StaticFiles(directory = "chat", html = True))