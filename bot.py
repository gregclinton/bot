from fastapi import FastAPI, Request, Query, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import chat
import httpx
import os
import random
import string

app = FastAPI(default_response_class=PlainTextResponse)

threads = {}

@app.post('/threads')
async def post_thread():
    id = ''.join(random.choices(string.ascii_lowercase, k = 32))
    threads[id] = await chat.reset({ "user": "me", "assistant": "hal" })
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
        await chat.reset(threads.pop(id))
    return "ok"

@app.delete('/threads/{id}/messages')
async def delete_messages(id: str):
    await chat.reset(threads[id])
    return "ok"

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

app.mount("/assistants", StaticFiles(directory = "assistants"))

app.mount("/", StaticFiles(directory = "client", html = True))
