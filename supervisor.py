from langgraph.graph import StateGraph, END, MessagesState
from typing import Literal
from typing_extensions import TypedDict
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver

def create(llm, agents):
    members = " or ".join(agents.keys())

    prompt = f"If you see {END}, set next to {END}, otherwise set next to one of {members} as appropriate."

    class AgentState(MessagesState):
        next: str

    def supervisor(state):
        class Router(TypedDict): next: Literal[*(list(agents.keys()) + [END])]
        return llm.with_structured_output(Router).invoke([SystemMessage(prompt)] + state["messages"])

    builder = StateGraph(AgentState)
    builder.add_node("supervisor", supervisor)
    builder.add_conditional_edges("supervisor", lambda state: state["next"])
    builder.add_edge("supervisor", END)

    for name, node in agents.items():
        builder.add_node(name, node)
        builder.add_edge(name, "supervisor")

    builder.set_entry_point("supervisor")
    return builder.compile(checkpointer=MemorySaver())