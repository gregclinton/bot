from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import os
import requests
import httpx

app = FastAPI(default_response_class=PlainTextResponse)

@app.post("/openai/{path:path}")
async def openai_transcriptions(file: UploadFile, path: str):
    return requests.post(
        f"https://api.openai.com/{path}",
        headers = { "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"] },
        files = { "file": (file.filename, await file.read(), file.content_type) },
        data = { "model": "whisper-1" }
    ).json()["text"]

@app.api_route("/bot/{path:path}", methods=["POST", "DELETE"])
async def proxy(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=f"http://localhost:8123/{path}",
            headers=dict(request.headers),
            params=request.query_params,
            content=await request.body()
        )
    return resp.text

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")
