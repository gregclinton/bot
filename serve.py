# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root company:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

from fastapi import FastAPI, Request
from messages import Messages, Message
import os
import company

msgs = "sephora.calls.txt"

app = FastAPI()

@app.post('/company/messages/{account}')
async def post_message(req: Request, account: str):
    prompt = (await req.json())['prompt']
    Messages.append_string_to_file(msgs, Message(account, "Sales", prompt).to_string())
    return { "content": company.invoke() }

@app.delete('/company/messages/{account}')
async def delete_messages(account: str):
    if os.path.exists(msgs):
        os.remove(msgs)
    return 'ok'