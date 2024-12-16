# poor man's nginx

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import requests

load_dotenv("keys")

app = FastAPI(default_response_class=PlainTextResponse)

@app.post("/openai/v1/audio/transcriptions")
async def speech(file: UploadFile):
    return requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers = { "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"] },
        files = { "file": (file.filename, await file.read(), file.content_type) },
        data = { "model": "whisper-1" }
    ).json()["text"]

url = lambda path: f"http://hal:8123/{path}"

@app.post("/bot/{path:path}")
async def proxy_bot(request: Request, path: str):
    return requests.post(url(path), data = (await request.body())).text

@app.delete("/bot/{path:path}")
async def proxy_bot(request: Request, path: str):
    return requests.delete(url(path), data = (await request.body())).text

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")
