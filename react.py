# sudo docker run -p 2024:2024 -v `pwd`:/root -w /root agent:latest langgraph dev

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import SystemMessage, HumanMessage
import os
from threads import thread

def get_model(model, temperature, instructions, tools):
    def call_model(state: MessagesState):
        llm = ChatOpenAI(model = model, temperature = 0).bind_tools(tools)
        return {'messages': llm.invoke([SystemMessage(instructions)] + state['messages'])}
    return call_model

class React:
    def __init__(self, instructions, tools, model="gpt-4o-mini", temperature=0):
        workflow = StateGraph(MessagesState)
        workflow.add_node('agent', get_model(model, temperature, instructions, tools))
        workflow.add_node('tools', ToolNode(tools = tools))
        workflow.add_conditional_edges('agent', tools_condition)
        workflow.add_edge('tools', 'agent')
        workflow.set_entry_point('agent')
        self.graph = workflow.compile(checkpointer = MemorySaver())

    def run(self, prompt):
        for event in self.graph.stream({"messages": [('user', prompt)]}, thread(), stream_mode = 'values'):
            pass

        return event['messages'][-1].content