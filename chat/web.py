from fastapi import FastAPI, Response, Request, Cookie
from fastapi.staticfiles import StaticFiles
import messages
import time
import asyncio
import secrets

app = FastAPI()

def get_account(session):
    # for now -- your system should implement
    return "TLG143623" if session else None

@app.post('/messages')
async def post_message(req: Request, session: str = Cookie(None)):
    msg = await req.json()
    account = get_account(session)
    if account:
        messages.post(account, "", msg["body"])
    return "ok"

@app.get("/messages")
async def get_messages(response: Response, session: str = Cookie(None), after: float = 0):
    posts = []
    start = time.time()

    if not session:
        # for now -- your system should implement
        session = secrets.token_hex(16)
        response.set_cookie(key="session", value = session, httponly = True)

    account = get_account(session)
    if account:
        while not posts and time.time() - start < 60:
            for frm, body, timestamp in messages.chat(account, after):
                posts.append({"from": frm, "body": body, "timestamp": timestamp})
            await asyncio.sleep(0.2)

    return posts

app.mount("/", StaticFiles(directory = "chat", html = True))