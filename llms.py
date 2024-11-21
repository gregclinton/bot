from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage

def get(model, temperature, instructions, tools):
    def call_model(state):
        llm = ChatOpenAI(model = model, temperature = 0).bind_tools(tools)
        return {'messages': llm.invoke([SystemMessage(instructions)] + state['messages'])}
    return call_model