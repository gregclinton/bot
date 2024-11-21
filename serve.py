# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root agent:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

from react import React
import threads
from tools import shell, search
from fastapi import FastAPI, Request

app = FastAPI()

graph = React("""
Your name is Simon. Do your best.
""", [
    shell,
    search,
])

@app.post('/prompts')
async def post_prompt(req: Request):
    return { "content":  graph.run((await req.json())['prompt']) }

@app.delete('/thread/current')
async def delete_thread():
    threads.delete_thread()

@app.delete('/prompts/last')
async def delete_last_prompt():
    graph.delete_last_prompt()