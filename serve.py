from fastapi import FastAPI, Request
from company import invoke

app = FastAPI()

@app.post('/company/messages/{caller}')
async def post_message(req: Request, caller: str):
    return invoke(caller, (await req.json())['prompt'])