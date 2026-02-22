from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import chat
import random
import string
import tool

app = FastAPI(default_response_class=PlainTextResponse)

threads = {}

# the following three endpoints are required for a bot
# they allow something similar to dialing a phone number, talking to the bot and then hanging up

@app.post('/threads')
async def post_thread():
    id = ''.join(random.choices(string.ascii_lowercase, k = 32))
    threads[id] = chat.create()
    return id

@app.post('/threads/{id}/messages')
async def post_message(req: Request, id: str):
    if id in threads:
        return await chat.run((await req.body()).decode("utf-8"), threads[id])
    else:
        return "Connection has ended."

@app.delete('/threads/{id}')
async def delete_thread(id: str):
    if id in threads:
        await tool.clear(threads.pop(id))
    return "ok"

app.mount("/", StaticFiles(directory = "client", html = True))

@app.on_event("shutdown")
async def stop():
    print("Stopping threads...", flush = True)
    for thread in threads.values():
        await tool.clear(thread)
    print("Threads stopped.", flush = True)