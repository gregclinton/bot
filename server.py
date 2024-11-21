# sudo docker run -p 8123:8123 -v `pwd`:/root -w /root agent:latest uvicorn server:app --host 0.0.0.0 --port 8123 --reload

from simon import graph
from langchain.schema import HumanMessage
from fastapi import FastAPI, Request

app = FastAPI()

thread_id = 1
thread = {
    'configurable': {'thread_id': str(thread_id)},
    'recursion_limit': 100
}

@app.delete('/thread/current')
async def delete_thread():
    global thread, thread_id
    thread_id += 1
    thread = {
        'configurable': {'thread_id': str(thread_id)},
        'recursion_limit': 10
    }

@app.delete('/prompts/last')
async def delete_last_prompt():
    msgs = graph.get_state(thread).values['messages']

    while not isinstance(msgs[-1], HumanMessage):
        msgs.pop()

    msgs.pop()

@app.post('/prompts')
async def post_prompt(req: Request):
    for event in graph.stream({"messages": [('user', (await req.json())['prompt'])]}, thread, stream_mode = 'values'):
        pass

    return event['messages'][-1]