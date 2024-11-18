from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.tools import TavilySearchResults
import subprocess
from dotenv import load_dotenv

load_dotenv('keys')

model = 'gpt-4o-mini'
temperature = 0

def build_graph():
    search = TavilySearchResults(
        max_results=2,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
        include_images=False
    )

    def shell(line):
        """
            run a shell command
        """
        print(line, flush = True)
        return subprocess.run(line, shell = True, capture_output = True, text = True).stdout

    def set_model(name):
        """
            gpt-4o, gpt-4o-mini or claude-3-5-sonnet-20241022
        """
        global model
        print(name, flush = True)
        model = name

    def set_temperature(x):
        """
            floating point number from 0.0 to 1.0
        """
        global temperature
        print(x, flush = True)
        temperature = x

    tools = [search, shell, set_model, set_temperature]

    def call_model(state: MessagesState):
        if model.startswith('claude'):
            llm = ChatAnthropic(model = model, temperature = temperature)
        else:
            llm = ChatOpenAI(model = model, temperature = temperature)
        
        llm = llm.bind_tools(tools)
        instructions = SystemMessage(content = r"""Your name is Simon.""")
        return {'messages': llm.invoke([instructions] + state['messages'])}

    workflow = StateGraph(MessagesState)
    workflow.add_node('agent', call_model)
    workflow.add_node('tools', ToolNode(tools = tools))
    workflow.add_conditional_edges('agent', tools_condition)
    workflow.add_edge('tools', 'agent')
    workflow.set_entry_point('agent')
    return workflow.compile(checkpointer = MemorySaver())

from fastapi import FastAPI, Request

app = FastAPI()

graph = build_graph()

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
    prompt = (await req.json())['prompt']

    for event in graph.stream({"messages": [('user', prompt)]}, thread, stream_mode = 'values'):
        pass

    msg = event['messages'][-1]
 
    return {
        'content': msg.content,
        'model': model,
        'temperature': temperature,
    }
