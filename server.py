# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root agent:latest uvicorn server:app --host 0.0.0.0 --port 8123 --reload

import graphs
from tools import shell, search
from fastapi import FastAPI, Request

app = FastAPI()

graphs.react("simon", """
Your name is Simon. Do your best.
""", [
    shell,
    search,
])

@app.post('/prompts')
async def post_prompt(req: Request):
    return { "content":  graphs.run("simon", (await req.json())['prompt']) }

@app.delete('/thread/current')
async def delete_thread():
    graphs.delete_thread()

@app.delete('/prompts/last')
async def delete_last_prompt():
    graphs.delete_last_prompt("simon")