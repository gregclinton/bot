# poor man's nginx
# export OPENAI_API_KEY=xxx
# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=example.com"
# uvicorn proxy:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import os
import requests

app = FastAPI(default_response_class=PlainTextResponse)

@app.post("/openai/v1/audio/transcriptions")
async def openai_transcriptions(file: UploadFile):
    return requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers = { "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"] },
        files = { "file": (file.filename, await file.read(), file.content_type) },
        data = { "model": "whisper-1" }
    ).json()["text"]

url = lambda path: f"http://hal:8123/{path}"

@app.post("/bot/{path:path}")
async def post_to_hal(request: Request, path: str):
    return requests.post(url(path), data = (await request.body())).text

@app.delete("/bot/{path:path}")
async def delete_from_hal(request: Request, path: str):
    return requests.delete(url(path), data = (await request.body())).text

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")
