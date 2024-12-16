from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import httpx

load_dotenv("keys")

app = FastAPI()

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")

@app.api_route("/openai/{path:path}", methods = ["GET", "POST", "PUT", "DELETE"])
async def proxy_openai(request: Request, path: str):
    url = f"https://api.openai.com/{path}"
    headers = dict(request.headers)
    headers["Authorization"] = "Bearer " + os.environ["OPENAI_API_KEY"]
    async with httpx.AsyncClient() as client:
        response  =  await client.request(
            request.method, url, headers = headers, content = await request.body()
        )
    return JSONResponse(content = response.json(), status_code = response.status_code)

@app.api_route("/bot/{path:path}", methods = ["GET", "POST", "PUT", "DELETE"])
async def proxy_bot(request: Request, path: str):
    url  =  f"http://127.0.0.1:8123/{path}"
    async with httpx.AsyncClient() as client:
        response  =  await client.request(
            request.method, url, headers = dict(request.headers), content = await request.body()
        )
    return JSONResponse(content = response.json(), status_code = response.status_code)
