from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import pkce
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

# https://fhir.epic.com/Developer/Apps
# https://open.epic.com/MyApps/endpoints
base_url = "https://fhir.epic.com/interconnect-fhir-oauth" # sandbox
base_url = "https://fhir.kp.org/service/ptnt_care/EpicEdiFhirRoutingSvc/v2014/esb-envlbl/212" # production
base_redirect_uri = "https://192.168.1.13/oauth"

@app.get("/oauth/{name}/login")
async def login(name: str):
    code_verifier, code_challenge = pkce.generate()
    os.environ[f"{name.upper()}_CODE_VERIFIER"] = code_verifier
    params = {
        "response_type": "code",
        "client_id": os.environ[f"{name.upper()}_CLIENT_ID"],
        "redirect_uri": f"{base_redirect_uri}/{name}",
        "scope": "patient/*.read",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": "random_state_string",
        "iss": f"{base_url}/api/FHIR/R4"
    }
    return RedirectResponse(f"{base_url}/oauth2/authorize?{ '&'.join(f'{k}={v}' for k, v in params.items()) }")

@app.get("/oauth/{name}")
async def callback(request: Request, name: str):
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(status_code = 400, detail = "Missing code")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{base_url}/oauth2/token",
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": f"{base_redirect_uri}/{name}",
                "client_id": os.environ[f"{name.upper()}_CLIENT_ID"],
                "code_verifier": os.environ[f"{name.upper()}_CODE_VERIFIER"]
            }
        )
        res.raise_for_status()
        return res.json()["access_token"]

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")
