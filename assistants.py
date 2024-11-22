from react import React
from langchain_community.tools import tool
import tools

assistants = {}

@tool
def cast(role, instructions, tools_csv):
    """
Cast an AI assistant with the specified role, instructions and a set of tools.
Tools is a comma separated string of tool names.
These may include search, cast, chroma and/or shell.
You must provide at least one tool.
    """
    assistants[role] = React(instructions, list(map(lambda t : tools.get(t), tools_csv.split(","))))
    return "success"

tools.put("cast", cast)

@tool
def call(role, prompt):
    """
Call the assistant with the specified role and prompt.
    """
    return assistants[role].run(prompt)

tools.put("call", call)