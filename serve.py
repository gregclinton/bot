from fastapi import FastAPI, Request
import company

app = FastAPI()

@app.post('/company/messages/{account}')
async def post_message(req: Request, account: str):
    return { "content": company.invoke(account, (await req.json())['prompt']) }