# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root agent:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

from react import React
from assistants import cast, call
import threads
from tools import shell, search
from fastapi import FastAPI, Request

app = FastAPI()

assistant = React("Do your best.", [shell, search, cast, call])

@app.post('/prompts')
async def post_prompt(req: Request):
    return { "content":  assistant.run((await req.json())['prompt']) }

@app.delete('/thread/current')
async def delete_thread():
    threads.delete_thread()

@app.delete('/prompts/last')
async def delete_last_prompt():
    assistant.delete_last_prompt()