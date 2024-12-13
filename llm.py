import requests
from importlib import import_module
import os
import json
from pprint import pprint
import inspect

def modules():
    for file in os.listdir("tools"):
        if file.endswith(".py"):
            yield import_module("tools." + file[:-3])

def reset(thread):
    thread["tools"] = {}

    for tool in modules():
        if hasattr(tool, "reset"):
            tool.reset(thread)
    return thread

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
                    args = json.loads(fn["arguments"])
                    args["thread"] = thread
                    output = import_module(f"tools.{tool}").run(**args)
                    print(f"tool {tool}:")

                    if tool in ['json']:
                        content = output
                        break
                    else:
                        del args["thread"]
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
