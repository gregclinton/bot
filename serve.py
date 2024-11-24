# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root agent:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

import threads
from tools import shell, search
from fastapi import FastAPI, Request
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from assistant import Assistant
import supervisor

app = FastAPI()

llm = ChatOpenAI(model = "gpt-4o-mini")
system_prompt = "At the end, indicate if you've finished your answer."

def call_model(state):
    return {"messages": [llm.invoke([SystemMessage(system_prompt)] + state["messages"])]}

assistant = Assistant(supervisor.create(llm, {
    "accountant": call_model,
    "rabbi": call_model,
    "admin": create_react_agent(llm, [shell, search], state_modifier=system_prompt),
}))

print(assistant.run("What is the size of chat.js in my current working directory?"))

@app.post('/prompts')
async def post_prompt(req: Request):
    return { "content": assistant.run((await req.json())['prompt']) }

@app.delete('/thread/current')
async def delete_thread():
    threads.delete_thread()

@app.delete('/prompts/last')
async def delete_last_prompt():
    assistant.delete_last_prompt()