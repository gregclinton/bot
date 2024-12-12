import requests
from dotenv import load_dotenv
from importlib import import_module
import os
import json
from pprint import pprint
import inspect

load_dotenv("keys")

def modules():
    tools = []

    for file in os.listdir("tools"):
        if file.endswith(".py"):
            tools.append(import_module("tools." + file[:-3]))
    return tools

def restart(thread):
    thread["tools"] = {}

    for tool in modules():
        if hasattr(tool, "restart"):
            tool.restart(thread)

def invoke(messages, thread={}):
    count = 0
    max_count = 10
    content = None
    tools = []

    for module in modules():
        params = {}

        for param, details in inspect.signature(module.run).parameters.items():
            if param != "thread":
                params[param] = {
                    "type": {"int": "integer", "str": "string"}[details.annotation.__name__],
                    "description": param
                }
        
        print(params, flush=True)

        tools.append({
            "type": "function",
            "function": {
                "name": module.__name__[6:], # strip "tools."
                "description": module.run.__doc__,
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": params,
                    "additionalProperties": False,
                    "required": list(params.keys())
                }
            }
        })

    while not content and count < max_count:
        count += 1
        message = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers = {
                'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
                'Content-Type': 'application/json',
            },
            json = {
                "model": thread.get("model", "gpt-4o"),
                "temperature": thread.get("temperature", 0),
                "messages": messages,
                "tools": tools,
                "tool_choice": "auto"
            }).json()["choices"][0]["message"]

        content = message.get("content")

        if not content:
            messages.append(message)

            for call in message.get("tool_calls", []):
                try:
                    fn = call["function"]
                    tool = fn["name"]
                    args = json.loads(fn["arguments"]) + [thread]
                    output = import_module(f"tools.{tool}").run(**args)
                    print(f"tool {tool}:")

                    if tool in ['json']:
                        content = output
                        break
                    else:
                        pprint(args)
                        print(output)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "name": tool,
                            "content": output
                        })
                except Exception as e:
                    return str(e)

    return content or "Could you rephrase that, please?"
