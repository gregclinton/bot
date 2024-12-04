import requests
from dotenv import load_dotenv
import os

load_dotenv("keys")

counter = 0

def reset_counter():
    global counter
    counter = 0

def invoke(messages):
    global counter

    counter += 1
    completion = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
            'Content-Type': 'application/json',
        },
        json = {
            "model": "gpt-4o",
            "temperature": 0,
            "messages": messages,
        }
    ).json()["choices"][0]["message"]["content"]

    return completion