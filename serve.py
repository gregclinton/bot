# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root company:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

from fastapi import FastAPI, Request
from messages import Messages

company = "sephora"
calls = f"{company}.calls.txt"

app = FastAPI()

@app.get('/company/messages/{account}')
async def get_prompt(req: Request, account: str):
    return Messages.load(calls, lambda msg: account in (msg.sender, msg.recipient))

@app.post('/company/messages/{account}')
async def post_prompt(req: Request, account: str):
    prompt = (await req.json())['prompt']
    return 'ok'

@app.delete('/company/messages/{account}')
async def delete_thread(account: str):
    return 'ok'