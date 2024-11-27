from fastapi import FastAPI, Request
import company

app = FastAPI()

    @app.post('/company/{company}/messages/{caller}')
async def post_message(req: Request, company:str, caller: str):
    return { "content": company.invoke(company, caller, (await req.json())['prompt']) }