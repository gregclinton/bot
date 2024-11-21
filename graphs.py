# sudo docker run -p 2024:2024 -v `pwd`:/root -w /root agent:latest langgraph dev

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

assistants = {}

load_dotenv('keys')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'

def get_model(model, temperature, instructions, tools):
    def call_model(state: MessagesState):
        llm = ChatOpenAI(model = model, temperature = 0).bind_tools(tools)
        return {'messages': llm.invoke([SystemMessage(instructions)] + state['messages'])}
    return call_model

def react(assistant_name, instructions, tools, model = 'gpt-4o-mini', temperature = 0):
    os.environ['LANGCHAIN_PROJECT'] = assistant_name

    workflow = StateGraph(MessagesState)
    workflow.add_node('agent', get_model(model, temperature, instructions, tools))
    workflow.add_node('tools', ToolNode(tools = tools))
    workflow.add_conditional_edges('agent', tools_condition)
    workflow.add_edge('tools', 'agent')
    workflow.set_entry_point('agent')
    assistants[assistant_name] = workflow.compile(checkpointer = MemorySaver())

thread_id = 1

def thread():
    return  {
        'configurable': {'thread_id': str(thread_id)},
        'recursion_limit': 100
    }

def run(assistant_name):
    for event in assistants[assistant_name].stream({"messages": [('user', prompt)]}, thread(), stream_mode = 'values'):
        pass

    return event['messages'][-1].content

def delete_thread():
    global thread_id
    thread_id += 1

def delete_last_prompt(assistant_name):
    msgs = assistants[assistant_name].get_state(thread()).values['messages']

    while not isinstance(msgs[-1], HumanMessage):
        msgs.pop()

    msgs.pop()