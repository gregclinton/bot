# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root agent:latest uvicorn server:app --host 0.0.0.0 --port 8123 --reload

import simon, graphs
from fastapi import FastAPI, Request

app = FastAPI()

@app.post('/prompts')
async def post_prompt(req: Request):
    return { "content":  graphs.run((await req.json())['prompt']) }

@app.delete('/thread/current')
async def delete_thread():
    graphs.delete_thread()

@app.delete('/prompts/last')
async def delete_last_prompt():
    graphs.delete_last_prompt()