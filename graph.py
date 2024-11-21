from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from threads import thread

class Graph:
    def __init__(self):
        self.graph = None

    def run(self, prompt):
        for event in self.graph.stream({"messages": [('user', prompt)]}, thread(), stream_mode = 'values'):
            pass

        return event['messages'][-1].content

    def delete_last_prompt():
        msgs = self.graph.get_state(thread()).values['messages']

        while not isinstance(msgs[-1], HumanMessage):
            msgs.pop()

        msgs.pop()

    @staticmethod
    def get_model(model, temperature, instructions, tools):
        def call_model(state):
            llm = ChatOpenAI(model = model, temperature = 0).bind_tools(tools)
            return {'messages': llm.invoke([SystemMessage(instructions)] + state['messages'])}
        return call_model
