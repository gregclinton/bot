from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import messages

app = FastAPI(default_response_class=PlainTextResponse)

@app.post('/messages')
async def post_message(req: Request):
    messages.post("CX143623", "Hal", req.body)
    return "OK"

@app.get('/messages')
async def get_messages():
    text = ""
    for msg in messages.inbox("CX143623"):
        text = msg.body

    return text

app.mount("/", StaticFiles(directory = "client", html = True))