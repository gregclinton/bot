# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

from langgraph.graph import MessagesState
from langchain_openai import ChatOpenAI
from typing import Literal
from typing_extensions import TypedDict
from dotenv import load_dotenv

load_dotenv('keys')

class AgentState(MessagesState):
    next: str

members = ["researcher", "coder"]
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
    next = llm.with_structured_output(Router).invoke(messages)["next"]
    if next_ == "FINISH":
        next_ = END

    return {"next": next_}