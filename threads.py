import os
from dotenv import load_dotenv

load_dotenv('keys')

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_PROJECT'] = "play"

thread_id = 1

def thread():
    return  {
        'configurable': {'thread_id': str(thread_id)},
        'recursion_limit': 100
    }

def delete_thread():
    global thread_id
    thread_id += 1