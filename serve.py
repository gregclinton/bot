# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root company:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

from fastapi import FastAPI, Request
import company

app = FastAPI()

@app.post('/company/messages/{account}')
async def post_message(req: Request, account: str):
    return { "content": company.invoke(account, (await req.json())['prompt']) }