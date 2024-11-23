# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from dotenv import load_dotenv

load_dotenv('keys')

from langgraph.graph import StateGraph, END, MessagesState
from langchain_openai import ChatOpenAI
from typing import Literal
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage

class AgentState(MessagesState):
    next: str

members = ["rabbi", "accountant"]
options = members + ["FINISH"]

llm = ChatOpenAI(model = "gpt-4o-mini")

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal[*options]

def supervisor_node(state: AgentState) -> AgentState:
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH."
    )

    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    next_ = llm.with_structured_output(Router).invoke(messages)["next"]
    if next_ == "FINISH":
        next_ = END

    return {"next": next_}

def rabbi(state):
    return {"messages": [HumanMessage(content="To be good. FINISH", name="rabbi")]}

def accountant(state):
    return {"messages": [HumanMessage(content="In April. FINISH", name="accountant")]}

builder = StateGraph(AgentState)
builder.add_node("supervisor", supervisor_node)
builder.add_node("rabbi", rabbi)
builder.add_node("accountant", accountant)

for member in members:
    builder.add_edge(member, "supervisor")

builder.add_conditional_edges("supervisor", lambda state: state["next"])
builder.set_entry_point("supervisor")

graph = builder.compile()

for s in graph.stream({"messages": [("user", "When do I pay my taxes?")]}, subgraphs = True):
    print(s)
    print("----")