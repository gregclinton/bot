from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import messages
import worker
import time
import asyncio

app = FastAPI()

@app.post('/messages')
async def post_message(req: Request):
    msg = await req.json()
    messages.post(msg["from"], msg["to"], msg["body"])
    return "ok"

@app.get("/messages/{worker}/{me}")
async def get_messages(worker: str, me: str, timestamp: int = 0, timeout: int = 10):
    results = []
    start = time.time()
    folder = worker.accounts / me

    while not results:
        for paath in folder.iterdir():
            ts, frm, to = path.name.split("|")
            ts = int(ts)
            if ts > timestamp:
                body = path.read_text()
                results.append({"from": frm, "body": body, "timestamp": ts})
        if results or time.time() - start > timeout:
            break
        await asyncio.sleep(0.2)

    return results

app.mount("/", StaticFiles(directory = "chat", html = True))