from fastapi import Request
from fastapi.responses import RedirectResponse
import os
import httpx
import base64, hashlib, secrets

provider = ""

def run(app):
    # https://fhir.epic.com/Developer/Apps
    # https://open.epic.com/MyApps/endpoints
    # https://hl7.org/fhir/smart-app-launch/app-launch.html
    # https://hl7.org/fhir/smart-app-launch/1.0.0/scopes-and-launch-context/

    base_url = {
        "kp": "https://fhir.kp.org/service/ptnt_care/EpicEdiFhirRoutingSvc/v2014/esb-envlbl/212",
        "providence": "https://haikuwa.providence.org/fhirproxy",
        "smile": "https://epicproxy.et1079.epichosted.com/FHIRProxy",
    }

    redirect_uri = "https://192.168.1.13/oauth/epic"

    @app.get("/oauth/epic/{name}/login")
    async def login(name: str):
        global provider
        provider = name
        os.environ["EPIC_CODE_VERIFIER"] = code_verifier = secrets.token_urlsafe(64)
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode()

        return RedirectResponse(f"{base_url[provider]}/oauth2/authorize?" + "&".join(f"{k}={v}" for k, v in {
            "response_type": "code",
            "client_id": os.environ["EPIC_CLIENT_ID"],
            "redirect_uri": redirect_uri,
            "state": "iuy24oi524o5u2i45y5u254hehwfh4oh4h4lhf4dghsad3",
            "scope": "patient/*.read",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "iss": f"{base_url[provider]}/api/FHIR/R4",
        }.items()))

    @app.get("/oauth/epic")
    async def callback(req: Request):
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{base_url[provider]}/oauth2/token", data = {
                "grant_type": "authorization_code",
                "code": req.query_params.get("code"),
                "redirect_uri": redirect_uri,
                "client_id": os.environ["EPIC_CLIENT_ID"],
                "code_verifier": os.environ["EPIC_CODE_VERIFIER"],
            })
            res.raise_for_status()
            with open(f"auth.json.epic.{provider}", "w") as f:
                f.write(res.text)
            return "You are now logged in. You can close this tab."
