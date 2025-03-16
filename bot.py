from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import chat

app = FastAPI(default_response_class=PlainTextResponse)

threads = {}

@app.post('/threads/{id}/messages')
async def post_message(req: Request, id: str):
    return chat.run((await req.body()).decode("utf-8"), threads[id])

@app.delete('/threads/{id}')
async def delete_thread(id: str):
    chat.reset(threads[id])
    return "success"

@app.delete('/threads/{id}/messages')
async def delete_messages(id: str):
    chat.reset(threads[id])
    return "success"

@app.delete('/threads/{id}/messages/last')
async def delete_last_message(id: str):
    chat.back(threads[id])
    return "success"

@app.post('/threads')
async def post_thread():
    id = str(10000 + len(threads))
    threads[id] = chat.reset({ "user": "me", "assistant": "hal" })
    return id