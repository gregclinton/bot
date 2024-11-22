from langgraph.graph import StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv('keys')

def call_model(state):
    return {'messages': ChatOpenAI(model = "gpt-4o-mini").invoke(state['messages'])}

workflow = StateGraph(MessagesState)
workflow.add_node('agent', call_model)
workflow.set_entry_point('agent')
graph = workflow.compile(checkpointer = MemorySaver())


prompt = "does flower rhyme with poor"
thread = {'configurable': {'thread_id': "1"},}
for event in graph.stream({"messages": [('user', prompt)]}, thread, stream_mode = 'values'):
    pass

print(event['messages'][-1].content)
