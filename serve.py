# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root agent:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

import threads
from tools import shell, search
from fastapi import FastAPI, Request
from langgraph.graph import END
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from assistant import Assistant
import supervisor

app = FastAPI()

llm = ChatOpenAI(model = "gpt-4o-mini")
assistant = Assistant(supervisor.create(llm, {
    "agent": create_react_agent(llm, [shell, search], state_modifier=f"Preface your response with {END}."),
}))

print(assistant.run('hello'))

@app.post('/prompts')
async def post_prompt(req: Request):
    return { "content": assistant.run((await req.json())['prompt']) }

@app.delete('/thread/current')
async def delete_thread():
    threads.delete_thread()

@app.delete('/prompts/last')
async def delete_last_prompt():
    assistant.delete_last_prompt()