from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import os
import httpx

app = FastAPI(default_response_class=PlainTextResponse)

@app.api_route("/bot/{path:path}", methods = ["POST", "DELETE"])
async def bot_proxy(request: Request, path: str):
    async with httpx.AsyncClient(timeout = 60) as client:
        return (await client.request(
            method = request.method,
            url = f"http://localhost:8123/{path}",
            headers = dict(request.headers),
            params = request.query_params,
            content = await request.body()
        )).text

@app.post("/transcription")
async def transcription(file: UploadFile):
    async with httpx.AsyncClient(timeout = 60) as client:
        return (await client.post(
            url = f"https://api.groq.com/openai/v1/audio/transcriptions",
            headers = { "Authorization": "Bearer " + os.environ["GROQ_API_KEY"] },
            files = { "file": (file.filename, await file.read(), file.content_type) },
            data = { 
                "model": "whisper-large-v3-turbo",
                "response_format": "text" 
            }
        )).text

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")
