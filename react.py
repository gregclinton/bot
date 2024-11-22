from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from assistant import Assistant

class React(Assistant):
    def __init__(self, instructions, tools, model="gpt-4o-mini", temperature=0):
        super().__init__(instructions, tools, model, temperature) 
        workflow = StateGraph(MessagesState)
        workflow.add_node('agent', self.model)
        workflow.add_node('tools', ToolNode(tools = tools))
        workflow.add_conditional_edges('agent', tools_condition)
        workflow.add_edge('tools', 'agent')
        workflow.set_entry_point('agent')
        self.graph = workflow.compile(checkpointer = MemorySaver())