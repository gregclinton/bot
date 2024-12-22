import os, httpx, base64, hashlib, secrets

# https://fhir.epic.com/Developer/Apps
# https://open.epic.com/MyApps/endpoints
# https://github.com/settings/applications/2819909

def base_url(name):
    return {
        "epic": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2",
        "github": "https://github.com/login/oauth"
    }

def redirect(name):
    params = {
        "response_type": "code",
        "client_id": os.environ[f"{name.upper()}_CLIENT_ID"],
        "redirect_uri": f"https://192.168.1.13/oauth/{name}",
        "state": "nil",
    }

    secret = os.environ[f"{name.upper()}_CLIENT_SECRET"]

    if secret:
        params["client_secret"] = secret
    else:
        os.environ[f"{name.upper()}_CODE_VERIFIER"] = code_verifier = secrets.token_urlsafe(64)
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode()

        params.update({
            "scope": "patient/*.read",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "iss": base_url(name)
        })

    return f"{base_url(name)}/authorize?" + "&".join(f"{k}={v}" for k, v in params.items())

async def callback(code, name):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{base_url(name)}/oauth2/token",
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": f"https://192.168.1.13/oauth/{name}",
                "client_id": os.environ[f"{name.upper()}_CLIENT_ID"],
                "code_verifier": os.environ[f"{name.upper()}_CODE_VERIFIER"]
            }
        )
        res.raise_for_status()
        return res.json()["access_token"]
