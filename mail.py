# sudo docker run -v `pwd`:/root -w /root company:latest python3 mail.py

from dotenv import load_dotenv
import os

load_dotenv("keys")

def setup():
    headers = {
        'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
        'Content-Type': 'application/json',
        'OpenAI-Beta': 'assistants=v2'
    }

    base_url = 'https://api.openai.com/v1'

    import requests

    return (
         lambda path, data = {}: requests.post(f'{base_url}/{path}', json = data, headers = headers).json(),
         lambda path: requests.get(f'{base_url}/{path}', headers = headers).json()['data'],
         lambda path: requests.delete(f'{base_url}/{path}', headers = headers)
    )

post, get, nix = setup()
del setup