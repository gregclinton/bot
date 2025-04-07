from fastapi import FastAPI, Request, UploadFile, Query
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import chat
import httpx
import os
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

# the remaining endpoints are just for me to play around with

@app.delete('/threads/{id}/messages/last')
async def delete_last_message(id: str):
    chat.back(threads[id])
    return "ok"

@app.put('/threads/{id}/model')
async def put_model(id: str, provider: str = Query(...), model: str = Query(...)):
    chat.set_model(threads[id], provider, model)
    return "ok"

@app.post("/transcription")
async def transcription(file: UploadFile):
    async with httpx.AsyncClient(timeout = 60) as client:
        return (await client.post(
            url = f"https://api.groq.com/openai/v1/audio/transcriptions",
            headers = { "Authorization": "Bearer " + os.environ.get("GROQ_API_KEY") },
            files = { "file": (file.filename, await file.read(), file.content_type) },
            data = {
                "model": "whisper-large-v3-turbo",
                "response_format": "text"
            }
        )).text

app.mount("/", StaticFiles(directory = "client", html = True))

@app.on_event("shutdown")
async def stop():
    print("Stopping threads...", flush = True)
    for thread in threads.values():
        await tool.clear(thread)
    print("Threads stopped.", flush = True)