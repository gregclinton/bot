from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from graph import Graph

class React(Graph):
    def __init__(self, instructions, tools, model="gpt-4o-mini", temperature=0):
        workflow = StateGraph(MessagesState)
        workflow.add_node('agent', Graph.get_model(model, temperature, instructions, tools))
        workflow.add_node('tools', ToolNode(tools = tools))
        workflow.add_conditional_edges('agent', tools_condition)
        workflow.add_edge('tools', 'agent')
        workflow.set_entry_point('agent')
        self.graph = workflow.compile(checkpointer = MemorySaver())