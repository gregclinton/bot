# sudo docker run -p 2024:2024 -v `pwd`:/root -w /root agent:latest langgraph dev

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

load_dotenv('keys')

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = "play"

thread_id = 1

def thread():
    return  {
        'configurable': {'thread_id': str(thread_id)},
        'recursion_limit': 100
    }

def delete_thread():
    global thread_id
    thread_id += 1

def delete_last_prompt(assistant_name):
    msgs = assistants[assistant_name].get_state(thread()).values['messages']

    while not isinstance(msgs[-1], HumanMessage):
        msgs.pop()

    msgs.pop()