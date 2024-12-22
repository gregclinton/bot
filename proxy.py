from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import oauth
import httpx

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

@app.get("/oauth/{name}/login")
async def login(name: str):
    return RedirectResponse(oauth.redirect(name))

@app.get("/oauth/{name}")
async def callback(req: Request, name: str):
    return oauth.callback(req.query_params.get("code"), name, str(req.url).split("?")[0])

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")
