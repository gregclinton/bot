from fastapi import FastAPI, Response, Request, Cookie
from fastapi.staticfiles import StaticFiles
import messages
import time
import asyncio
import secrets
import account
from pathlib import Path

app = FastAPI()

def get_account(session):
    # you should implement this yourself
    folder = Path("sessions") / session
    folder.mkdir(parents = True, exist_ok = True)
    path = folder / "account"

    if path.exists():
        account = path.read_text()
    else:
        account = account.create()
        path.write_text(account)

    return account

@app.post("/messages")
async def post_message(req: Request, session: str = Cookie(None)):
    messages.post(get_account(session), "", (await req.json())["body"])
    return "ok"

@app.get("/messages")
async def get_messages(response: Response, after: float, session: str = Cookie(None)):
    posts = []

    if not session:
        # for now -- your system should implement
        response.set_cookie(key="session", value = secrets.token_hex(16), httponly = True)
    else:
        start = time.time()
        while not posts and time.time() - start < 60:
            for frm, body, timestamp in messages.chat(get_account(session), after):
                posts.append({"from": frm, "body": body, "timestamp": timestamp})
            await asyncio.sleep(0.2)

    return posts

app.mount("/", StaticFiles(directory = "chat", html = True))