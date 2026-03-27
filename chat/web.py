from fastapi import FastAPI, Response, Request, Cookie
from fastapi.staticfiles import StaticFiles
import messages
import time
import asyncio
import secrets
import account
from pathlib import Path

app = FastAPI()
sessions = Path("sessions")

def get_session(res, session):
    if not session:
        session = secrets.token_hex(16)
        (sessions / session).mkdir(parents = True, exist_ok = True)
    res.set_cookie(key="session", value = session, max_age = 31536000, httponly = True)
    return session

def get_account(session):
    path = sessions / session / "account"

    if path.exists():
        acct = path.read_text()
    else:
        acct = account.create()
        path.write_text(acct)

    return acct

@app.post("/messages")
async def post_message(req: Request, res: Response, session: str = Cookie(None)):
    messages.post(get_account(get_session(res, session)), "", (await req.json())["body"])
    return "ok"

@app.get("/messages")
async def get_messages(res: Response, after: float, session: str = Cookie(None)):
    posts = []

    if session:
        start = time.time()
        while not posts and time.time() - start < 60:
            for frm, body, timestamp in messages.chat(get_account(session), after):
                posts.append({"from": frm, "body": body, "timestamp": timestamp})
            await asyncio.sleep(0.2)

    get_session(res, session)
    return posts

app.mount("/", StaticFiles(directory = "chat", html = True))