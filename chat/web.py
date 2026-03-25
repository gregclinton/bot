from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import messages
import time
import asyncio
from worker import chat

app = FastAPI()

@app.post('/messages')
async def post_message(req: Request):
    msg = await req.json()
    messages.post(msg["from"], msg["to"], msg["body"])
    return "ok"

@app.get("/messages/{worker}/{account}")
async def get_messages(worker: str, account: str, after: float = 0):
    results = []
    start = time.time()

    while not results and time.time() - start < 60:
        for frm, body, timestamp in chat(worker, account, after):
            results.append({"from": frm, "body": body, "timestamp": timestamp})
        await asyncio.sleep(0.2)

    return results

app.mount("/", StaticFiles(directory = "chat", html = True))