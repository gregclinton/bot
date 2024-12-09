import requests
from dotenv import load_dotenv
from importlib import import_module
import os
import json
from pprint import pprint

load_dotenv("keys")

def invoke(messages, thread={}):
    count = 0
    max_count = 10
    content = None
    tools = []

    for file in os.listdir("tools"):
        if file.endswith(".py"):
            tool = file[:-3]
            meta = import_module(f"tools.{tool}").meta()
            params = meta["parameters"]
            params["type"] = "object"
            tools.append({
                "type": "function",
                "function": {
                    "name": tool,
                    "description": meta["description"],
                    "parameters": params
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
                    content = import_module(f"tools.{tool}").run(args, thread)
                    print(f"tool {tool}:")
                    pprint(args)
                    print(content)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "name": tool,
                        "content": content
                    })
                except Exception as e:
                    return str(e)

    return content or "Could you rephrase that, please?"
