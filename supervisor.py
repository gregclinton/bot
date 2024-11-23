from langgraph.graph import StateGraph, END, MessagesState
from typing import Literal
from typing_extensions import TypedDict
from langchain_core.messages import SystemMessage

# https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/#construct-graph

def create(llm, prompt, agents):
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