from fastapi import FastAPI, Request
from mall import invoke

app = FastAPI()

@app.post('/mall/messages/{caller}')
async def post_message(req: Request, caller: str):
    return invoke(caller, (await req.json())['prompt'])