from fastapi import FastAPI, Request
from company import invoke

app = FastAPI()

@app.post('/company/{company}/messages/{caller}')
async def post_message(req: Request, company: str, caller: str):
    return { "content": invoke(company, caller, (await req.json())['prompt']) }