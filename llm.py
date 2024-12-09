import requests
from dotenv import load_dotenv
import os

load_dotenv("keys")

def invoke(messages, tools=[], thread={}):
    data = {
        "model": thread.get("model", "gpt-4o"),
        "temperature": thread.get("temperature", 0),
        "messages": messages,
    }

    if tools:
        data["tools"] = tools
        data["tool_choice"] ="auto"

    return requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
            'Content-Type': 'application/json',
        },
        json = data
    ).json()["choices"][0]["message"]["content"]
