from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import os
import httpx
import epic

app = FastAPI(default_response_class=PlainTextResponse)

@app.api_route("/bot/{path:path}", methods = ["POST", "DELETE"])
async def bot_proxy(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        return (await client.request(
            method = request.method,
            url = f"http://localhost:8123/{path}",
            headers = dict(request.headers),
            params = request.query_params,
            content = await request.body()
        )).text

@app.post("/transcription")
async def transcription(file: UploadFile):
    async with httpx.AsyncClient() as client:
        return (await client.post(
            url = f"https://api.openai.com/v1/audio/transcriptions",
            headers = { "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"] },
            files = { "file": (file.filename, await file.read(), file.content_type) },
            data = { "model": "whisper-1", "language": "en", "response_format": "text" }
        )).text

epic.run(app)

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")
