from fastapi import FastAPI, Response, Request, Cookie
from fastapi.staticfiles import StaticFiles
import messages
import time
import asyncio
import secrets
import account

app = FastAPI()

@app.post("/messages")
async def post_message(req: Request, session: str = Cookie(None)):
    messages.post(account.get(session), "", (await req.json())["body"])
    return "ok"

@app.get("/messages")
async def get_messages(response: Response, after: float, session: str = Cookie(None)):
    posts = []

    if not session:
        # for now -- your system should implement
        response.set_cookie(key="session", value = secrets.token_hex(16), httponly = True)
    else:
        acct = account.get(session)
        start = time.time()
        while not posts and time.time() - start < 60:
            for frm, body, timestamp in messages.chat(acct, after):
                posts.append({"from": frm, "body": body, "timestamp": timestamp})
            await asyncio.sleep(0.2)

    return posts

app.mount("/", StaticFiles(directory = "chat", html = True))