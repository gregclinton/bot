# sudo docker run -v `pwd`:/root -w /root company:latest python3 mail.py

import requests
from dotenv import load_dotenv
import os

load_dotenv("keys")

def invoke(prompt):
    return requests.post(
        "https://api.openai.com/v1/chat/completions", 
        headers = {
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
            'Content-Type': 'application/json',
        },
        json = {
            "model": "gpt-4o-mini",
            "temperature": 0
            "messages": [{"role": "user", "content": prompt}],
        }
    ).json()["choices"][0]["message"]["content"]