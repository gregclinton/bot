# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root agent:latest uvicorn serve:app --host 0.0.0.0 --port 8123 --reload

import threads
from tools import shell, search
from fastapi import FastAPI, Request
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from threads import thread

app = FastAPI()

llm = ChatOpenAI(model = "gpt-4o-mini")
builder = StateGraph(MessagesState)
builder.add_node('agent', create_react_agent(llm, [shell, search], state_modifier="Do your best."))
builder.set_entry_point('agent')
graph = builder.compile(checkpointer = MemorySaver())

@app.post('/prompts')
async def post_prompt(req: Request):
    def run(prompt):
        for event in graph.stream({"messages": [('user', prompt)]}, thread(), stream_mode = 'values'):
            pass

        return event['messages'][-1].content
    return { "content": run((await req.json())['prompt']) }

@app.delete('/thread/current')
async def delete_thread():
    threads.delete_thread()

@app.delete('/prompts/last')
async def delete_last_prompt():
    assistant.delete_last_prompt()