from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import messages

app = FastAPI()

@app.post('/messages')
async def post_message(req: Request):
    msg = await req.json()
    messages.post(msg["frm"], msg["to"], msg["body"])
    return { "status": "ok" }

@app.get("/messages/{owner}")
async def get_messages(owner: str):
    return [msg.body for msg in messages.inbox(owner)]

app.mount("/", StaticFiles(directory = "client", html = True))