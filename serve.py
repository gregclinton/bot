# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root company:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

from fastapi import FastAPI, Request

app = FastAPI()

@app.get('/company/messages/{account}')
async def get_prompt(req: Request):
    return { "content": (await req.json())['prompt'] }

@app.post('/company/messages/{account}')
async def post_prompt(req: Request):
    return { "content": (await req.json())['prompt'] }

@app.delete('/company/messages/{account}')
async def delete_thread():
    return 'ok'