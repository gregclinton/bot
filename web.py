from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import messages
import time

app = FastAPI()

@app.post('/messages')
async def post_message(req: Request):
    msg = await req.json()
    messages.post(msg["frm"], msg["to"], msg["body"])
    return "ok"

@app.get("/messages/{to}")
async def get_messages(owner: str, timeout: int = 10):
    results = []
    start = time.time()

    while True:
        for frm, to, body, timestamp in messages.inbox(to):
            results.append(body)
        if results or time.time() - start > timeout:
            break
        else:
            time.sleep(0.2)

    return results

app.mount("/", StaticFiles(directory = "chat", html = True))