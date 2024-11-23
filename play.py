# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from dotenv import load_dotenv

load_dotenv('keys')

from langgraph.graph import StateGraph, END, MessagesState
from langchain_openai import ChatOpenAI
from typing import Literal
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage

# https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/#construct-graph

class AgentState(MessagesState):
    next: str

members = ["rabbi", "accountant"]
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

def accountant(state):
    return {"messages": [HumanMessage(content="You file your taxes on April 15.")]}

builder = StateGraph(AgentState)
builder.add_node("supervisor", supervisor)
builder.add_node("rabbi", rabbi)
builder.add_node("accountant", accountant)

for member in members:
    builder.add_edge(member, "supervisor")

builder.add_conditional_edges("supervisor", lambda state: state["next"])
builder.set_entry_point("supervisor")
graph = builder.compile()

for event in graph.stream({"messages": [("user", "When do I file my taxes?")]}):
    print(event)
    print("-----")