# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from dotenv import load_dotenv

load_dotenv('keys')

from langgraph.graph import StateGraph, END, MessagesState
from langchain_openai import ChatOpenAI
from typing import Literal
from typing_extensions import TypedDict
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from tools import shell

# https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/#construct-graph

class AgentState(MessagesState):
    next: str


llm = ChatOpenAI(model = "gpt-4o-mini")

rabbi = lambda state: {"messages": [HumanMessage(content="The meaning of life is to be good.")]}
admin = create_react_agent(llm, tools=[shell], state_modifier="You are an admin. Use the shell tool.")

builder = StateGraph(AgentState)
builder.add_node("rabbi", rabbi)
builder.add_node("admin", admin)

def supervise(builder):
    members = ["rabbi", "admin"]

    def supervisor(state):
        class Router(TypedDict): next: Literal[*(members + [END])]
        prompt = f"From {members} pick the more appropriate. Respond {END} when either has responded."
        return llm.with_structured_output(Router).invoke([SystemMessage(prompt)] + state["messages"])

    builder.add_node("supervisor", supervisor)
    builder.add_conditional_edges("supervisor", lambda state: state["next"])

    for member in members:
        builder.add_edge(member, "supervisor")

supervise(builder)
builder.set_entry_point("supervisor")
graph = builder.compile()

for event in graph.stream({"messages": [("user", "What is the meaning of life?")]}):
    print(event)
    print("-----")