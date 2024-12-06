import requests

def invoke(text, thread):
    base_url, prompt = text.split("\n")
    post = lambda path, data = {}: requests.post(f'{base_url}/{path}', json = data, headers = headers).json(),
    nix = lambda path: requests.delete(f'{base_url}/{path}', headers = headers)
    thread_id = post('threads')['id']
    response = post(f'threads/{thread_id}/messages', {
        'role': 'user',
        'content': prompt
    })["content"]
    nix(f'threads/{thread_id}/messages')
    return response
