from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from threads import thread

class Assistant:
    def __init__(self, instructions, tools, model, temperature):
        def call_model(state):
            llm = ChatOpenAI(model = model, temperature = 0).bind_tools(tools)
            return {'messages': llm.invoke([SystemMessage(instructions)] + state['messages'])}

        self.model = call_model
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
