from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import messages
import time
import asyncio

app = FastAPI()

@app.post('/messages')
async def post_message(req: Request):
    msg = await req.json()
    messages.post(msg["from"], msg["to"], msg["body"])
    return "ok"

@app.get("/messages/{to}")
async def get_messages(to: str, timeout: int = 10):
    results = []
    start = time.time()

    while True:
        for _, _, body, _ in messages.inbox(to):
            results.append(body)
        if results or time.time() - start > timeout:
            break
        await asyncio.sleep(0.2)

    return results

app.mount("/", StaticFiles(directory = "chat", html = True))