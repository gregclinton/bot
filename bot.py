from fastapi import FastAPI, Request, Query, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import chat
import os
import httpx

app = FastAPI(default_response_class=PlainTextResponse)

threads = {}

@app.put('/threads/{id}/model')
async def put_model(id: str, model: str = Query(...)):
    chat.set_model(threads[id], model)
    return "success"

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

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")

app.mount("/assistants", StaticFiles(directory = "assistants"), name = "assistants")
