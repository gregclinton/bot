# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from dotenv import load_dotenv

load_dotenv('keys')

from langgraph.graph import StateGraph, END, MessagesState
from langchain_openai import ChatOpenAI
from typing import Literal
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools import shell

# https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/#construct-graph

class AgentState(MessagesState):
    next: str

members = ["rabbi", "admin"]
options = members + ["FINISH"]

llm = ChatOpenAI(model = "gpt-4o-mini")

class Router(TypedDict):
    next: Literal[*options]

def supervisor(state):
    system_prompt = f"From {members} pick the more appropriate. Respond FINISH when either has responded."

    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    next_ = llm.with_structured_output(Router).invoke(messages)["next"]

    if next_ == "FINISH":
        next_ = END

    return {"next": next_}

def rabbi(state):
    return {"messages": [HumanMessage(content="The meaning of life is to be good.")]}

def admin(state):
    return {"messages": [HumanMessage(content="You file your taxes on April 15.")]}

admin = create_react_agent(llm, tools=[shell], state_modifier="You are an admin. Use the shell tool.")


builder = StateGraph(AgentState)
builder.add_node("supervisor", supervisor)
builder.add_node("rabbi", rabbi)
builder.add_node("admin", admin)

for member in members:
    builder.add_edge(member, "supervisor")

builder.add_conditional_edges("supervisor", lambda state: state["next"])
builder.set_entry_point("supervisor")
graph = builder.compile()

for event in graph.stream({"messages": [("user", "List files in my current working directory")]}):
    print(event)
    print("-----")