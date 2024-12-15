from fastapi import FastAPI, Request, APIRouter, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import chat
import os
import requests

load_dotenv("keys")

app = FastAPI(default_response_class=PlainTextResponse)
api = APIRouter(prefix="/bot")

threads = {}

@api.post('/threads/{id}/messages')
async def post_message(req: Request, id: str):
    return chat.run((await req.body()).decode("utf-8"), threads[id])

@api.delete('/threads/{id}')
async def delete_thread(id: str):
    chat.reset(threads[id])
    return "success"

@api.delete('/threads/{id}/messages')
async def delete_messages(id: str):
    chat.reset(threads[id])
    return "success"

@api.delete('/threads/{id}/messages/last')
async def delete_last_message(id: str):
    chat.back(threads[id])
    return "success"

@api.post('/threads')
async def post_thread():
    threads.clear() # heroku workaround
    id = str(10000 + len(threads))
    threads[id] = chat.reset({})
    return id

@api.post("/transcriptions")
async def speech_to_text(file: UploadFile):
    return requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers = { "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"] },
        files = { "file": (file.filename, await file.read(), file.content_type) },
        data = { "model": "whisper-1" }
    ).json()["text"]

app.include_router(api)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
