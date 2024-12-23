from fastapi import Request
from fastapi.responses import RedirectResponse
import os
import httpx

# https://github.com/settings/applications/2819909

def run(app):
    base_url = "https://github.com/login/oauth"

    @app.get("/oauth/github/login")
    async def login():
        return RedirectResponse(f"{base_url}/authorize?" + "&".join(f"{k}={v}" for k, v in {
            "client_id": os.environ["GITHUB_CLIENT_ID"],
            "scope": "read:user",
            "redirect_uri": "https://192.168.1.13/oauth/github",
        }.items()))

    @app.get("/oauth/github")
    async def callback(req: Request):
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{base_url}/access_token", data = {
                "code": req.query_params.get("code"),
                "client_id": os.environ["GITHUB_CLIENT_ID"],
                "client_secret": os.environ["GITHUB_CLIENT_SECRET"],
            })
            res.raise_for_status()
            with open("auth.json.github", "w") as f:
                f.write(res.text)
            return "You are now logged in. You can close this tab."
