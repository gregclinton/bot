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
import os

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = "play"

# https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/#construct-graph

def create_supervisor(llm, prompt, agents):
    class AgentState(MessagesState):
        next: str

    builder = StateGraph(AgentState)

    def supervisor(state):
        class Router(TypedDict): next: Literal[*(list(agents.keys()) + [END])]
        return llm.with_structured_output(Router).invoke([SystemMessage(prompt)] + state["messages"])

    builder.add_node("supervisor", supervisor)
    builder.add_conditional_edges("supervisor", lambda state: state["next"])

    for name, node in agents.items():
        builder.add_node(name, node)
        builder.add_edge(name, "supervisor")

    builder.set_entry_point("supervisor")
    return builder.compile()

llm = ChatOpenAI(model = "gpt-4o-mini")

agents = {
    "rabbi": lambda state: {"messages": [HumanMessage("The meaning of life is to be good.")]},
    "admin": create_react_agent(llm, [shell], state_modifier="You are an admin. Use the shell tool."),
}

graph = create_supervisor(llm, f"From {','.join(agents.keys())}, pick the more appropriate. Respond {END} when either has responded.", agents)

graph.invoke({"messages": [("user", "File size of chat.js in current working directory?")]})