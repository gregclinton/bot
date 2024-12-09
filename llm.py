import requests
from dotenv import load_dotenv
from importlib import import_module
import os
import json

load_dotenv("keys")

def invoke(messages, thread={}):
    count = 0
    max_count = 10
    content = None
    tools = []

    for file in os.listdir("tools"):
        if file.endswith(".py"):
            fn, text = import_module("tools." + file[:-3]).descriptions()
            tools.append({ 
                "type": "function",
                "function": {
                    "name": "shell",
                    "description": fn,
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "text": {
                            "type": "string",
                            "description": text
                        }
                        },
                        "required": ["text"]
                    }
                }
            })

    while not content and count < 10:
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

                    messages.append({
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "name": fn["name"],
                        "content": import_module("tools." + fn["name"]).run(json.loads(fn["arguments"])["text"], thread)
                    })
                except Exception as e:
                    return str(e)

    return content or "Could you rephrase that, please?"
