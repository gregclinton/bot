# sudo docker run -v `pwd`:/root -w /root agent:latest python3 play.py
# sudo docker run -v `pwd`:/root -w /root agent:latest langgraph dev

import os
from dotenv import load_dotenv

load_dotenv('keys')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = "play"

import supervisor
from langgraph.graph import END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools import shell

llm = ChatOpenAI(model = "gpt-4o-mini")

agents = {
    "rabbi": lambda state: {"messages": [HumanMessage("The meaning of life is to be good.")]},
    "admin": create_react_agent(llm, [shell], state_modifier="You are an admin. Use the shell tool."),
}

graph = supervisor.create(llm, f"From {','.join(agents.keys())}, pick the more appropriate. Respond {END} when either has responded.", agents)

graph.invoke({"messages": [("user", "File size of chat.js in current working directory?")]})