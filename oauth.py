import os, base64, hashlib, secrets, httpx

# https://fhir.epic.com/Developer/Apps
# https://open.epic.com/MyApps/endpoints

base_url = {
    # "eric": "https://fhir.epic.com/interconnect-fhir-oauth" # sandbox
    "eric": "https://fhir.kp.org/service/ptnt_care/EpicEdiFhirRoutingSvc/v2014/esb-envlbl/212", # production
}

base_redirect_uri = "https://192.168.1.13/oauth"

def redirect(name):
    os.environ[f"{name.upper()}_CODE_VERIFIER"] = code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode()

    return f"{base_url[name]}/oauth2/authorize?" + "&".join(f"{k}={v}" for k, v in {
        "response_type": "code",
        "client_id": os.environ[f"{name.upper()}_CLIENT_ID"],
        "redirect_uri": f"{base_redirect_uri}/{name}",
        "scope": "patient/*.read",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": "random_state_string",
        "iss": f"{base_url[name]}/api/FHIR/R4"
    }.items())

async def callback(code, name):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{base_url[name]}/oauth2/token",
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
