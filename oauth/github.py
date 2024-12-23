from fastapi import Request
from fastapi.responses import RedirectResponse
import os
import httpx

# https://github.com/settings/applications/2819909

def run(app):
    base_url = "https://github.com/login/oauth"
    redirect_uri = "https://192.168.1.13/oauth/github"

    @app.get("/oauth/github/login")
    async def login(name: str):
        return RedirectResponse(f"{base_url}/oauth2/authorize?" + "&".join(f"{k}={v}" for k, v in {
            "response_type": "code",
            "client_id": os.environ["GITHUB_CLIENT_ID"],
            "client_secret": os.environ["GITHUB_CLIENT_SECRET"],
            "redirect_uri": redirect_uri,
        }.items()))

    @app.get("/oauth/github")
    async def callback(req: Request):
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{base_url[provider]}/oauth2/token", data = {
                "grant_type": "authorization_code",
                "code": req.query_params.get("code"),
                "redirect_uri": redirect_uri,
                "client_id": os.environ["GITHUB_CLIENT_ID"],
            })
            res.raise_for_status()
            with open(f"auth.json.epic.{provider}", "w") as f:
                f.write(res.text)
            return "You are now logged in. You can close this tab."
