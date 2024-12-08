import requests
from dotenv import load_dotenv
import os

load_dotenv("keys")

def invoke(messages, thread={}):
    return requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
            'Content-Type': 'application/json',
        },
        json = {
            "model": thread.get("model", "gpt-4o"),
            "temperature": thread.get("temperature", 0),
            "messages": messages,
        }
    ).json()["choices"][0]["message"]["content"]
