# sudo docker run -p 2024:2024 -v `pwd`:/root -w /root agent:latest langgraph dev

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import SystemMessage, HumanMessage
import subprocess
import os
from dotenv import load_dotenv

load_dotenv('keys')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = 'simon'

def graph(system_instruction, tools):

    def call_model(state: MessagesState):
        llm = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0).bind_tools(tools)
        instructions = SystemMessage(content = system_instruction)
        return {'messages': llm.invoke([instructions] + state['messages'])}

    workflow = StateGraph(MessagesState)
    workflow.add_node('agent', call_model)
    workflow.add_node('tools', ToolNode(tools = tools))
    workflow.add_conditional_edges('agent', tools_condition)
    workflow.add_edge('tools', 'agent')
    workflow.set_entry_point('agent')
    return workflow.compile(checkpointer = MemorySaver())