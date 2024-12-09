import requests
from dotenv import load_dotenv
from importlib import import_module
import os

load_dotenv("keys")

tools = []
import_module("tools.shell").create(tools)

def invoke(messages, thread={}):
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

    calls = message.get("tool_calls")

    if calls:
        return "tool call"

    return message["content"]
