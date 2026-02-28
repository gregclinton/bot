from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import messages

app = FastAPI()

@app.post('/messages')
async def post_message(req: Request):
    messages.post("CX143623", "Hal", req.body)
    return { "status": "ok" }

@app.get('/messages')
async def get_messages():
    return [ msg.body for msg in messages.inbox("CX143623") ]

app.mount("/", StaticFiles(directory = "client", html = True))