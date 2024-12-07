import requests
from dotenv import load_dotenv
import os

load_dotenv("keys")

def invoke(messages, model=None, temperature=None):
    return requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
            'Content-Type': 'application/json',
        },
        json = {
            "model": model or "gpt-4o-mini",
            "temperature": temperature or 0,
            "messages": messages,
        }
    ).json()["choices"][0]["message"]["content"]
