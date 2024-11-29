import requests
from dotenv import load_dotenv
import os

load_dotenv("keys")

def reset_counter():
    global counter
    counter = 0

def invoke(instruction, prompt):
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
            "messages": [
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt}
            ],
        }
    ).json()["choices"][0]["message"]["content"]

    if False:
        print(f"Instruction: \n{instruction}\n")
        print(f"Prompt: \n{prompt}\n")
        print(f"Completion: \n{completion}\n")

    return completion