from react import React
from tools import search, shell
from langchain_community.tools import tool

assistants = {}

@tool
def cast(role, instructions, tools):
    """
Cast an AI assistant with the specified role, instructions and a set of tools.
Tools is a comma separated string of tool names.
These may include search, cast, chroma and/or shell.
You must provide at least one tool.
    """
    assistants[role] = React(instructions, list(map(lambda t : {"search": search, "shell": shell}[t], tools.split(","))))
    return "success"

@tool
def call(role, prompt):
    """
Call the assistant with the specified role and prompt.
    """
    return assistants[role].run(prompt)