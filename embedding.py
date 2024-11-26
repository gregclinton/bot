import requests
from dotenv import load_dotenv
import os

load_dotenv("keys")

def embed(text):
    return requests.post(
        "https://api.openai.com/v1/embeddings",
        headers = {
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
            'Content-Type': 'application/json',
        },
        json = {
            "model": "text-embedding-ada-002",
            "input": text,
        }
    ).json()["data"][0]["embedding"]