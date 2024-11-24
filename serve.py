# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root company:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

from fastapi import FastAPI, Request

app = FastAPI()

@app.post('/prompts')
async def post_prompt(req: Request):
    return { "content": assistant.run((await req.json())['prompt']) }

@app.delete('/thread/current')
async def delete_thread():
    pass