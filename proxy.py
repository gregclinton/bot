from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import httpx
import base64, hashlib, secrets

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
# https://hl7.org/fhir/smart-app-launch/app-launch.html

base_url = "https://fhir.kp.org/service/ptnt_care/EpicEdiFhirRoutingSvc/v2014/esb-envlbl/212"
redirect_uri = "https://192.168.1.13/oauth/epic"

@app.get("/oauth/epic/login")
async def login():
    os.environ["EPIC_CODE_VERIFIER"] = code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode()

    return RedirectResponse(f"{base_url}/oauth2/authorize?" + "&".join(f"{k}={v}" for k, v in {
        "response_type": "code",
        "client_id": os.environ["EPIC_CLIENT_ID"],
        "redirect_uri": redirect_uri,
        "state": "iuy24oi524o5u2i45y5u254hehwfh4oh4h4lhf4dghsad3",
        "scope": "patient.read",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "iss": f"{base_url}/api/FHIR/R4",
    }.items()))

@app.get("/oauth/epic")
async def callback(req: Request):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{base_url}/oauth2/token", data = {
            "grant_type": "authorization_code",
            "code": req.query_params.get("code"),
            "redirect_uri": redirect_uri,
            "client_id": os.environ["EPIC_CLIENT_ID"],
            "code_verifier": os.environ["EPIC_CODE_VERIFIER"],
        })
        res.raise_for_status()
        os.environ["EPIC_TOKEN"] = res.json()["access_token"]
        return "You are now logged in. You can close this tab."

app.mount("/", StaticFiles(directory = "client", html = True), name = "client")
