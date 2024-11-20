# sudo docker run -p 2024:2024 -v `pwd`:/root -w /root agent:latest langgraph dev

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.tools import TavilySearchResults
import subprocess
import os
from dotenv import load_dotenv

load_dotenv('keys')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = 'simon'

def build_graph():
    search = TavilySearchResults(
        max_results=2,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
        include_images=False
    )

    def shell(line):
        """
            run a shell command
        """
        print(line, flush = True)
        return subprocess.run(line, shell = True, capture_output = True, text = True).stdout

    tools = [search, shell]

    def call_model(state: MessagesState):
        llm = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0).bind_tools(tools)
        instructions = SystemMessage(content = r"""Your name is Simon.""")
        return {'messages': llm.invoke([instructions] + state['messages'])}

    workflow = StateGraph(MessagesState)
    workflow.add_node('agent', call_model)
    workflow.add_node('tools', ToolNode(tools = tools))
    workflow.add_conditional_edges('agent', tools_condition)
    workflow.add_edge('tools', 'agent')
    workflow.set_entry_point('agent')
    return workflow.compile(checkpointer = MemorySaver())