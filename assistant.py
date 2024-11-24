from langchain.schema import HumanMessage
from threads import thread

class Assistant:
    def __init__(self, graph):
        self.graph = graph

    def run(self, prompt):
        for event in self.graph.stream({"messages": [('user', prompt)]}, thread(), stream_mode = 'values'):
            pass

        return event['messages'][-1].content

    def delete_last_prompt():
        msgs = self.graph.get_state(thread()).values['messages']

        while not isinstance(msgs[-1], HumanMessage):
            msgs.pop()

        msgs.pop()
