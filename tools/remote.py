import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = { "Content-Type": "text/plain" }

name = __name__[6:] # strip "tools." 

def reset(thread):
    thread["tools"] = tools = thread.get("tools", {})
    tools[name] = data = tools.get(name, {})
    data["remotes"] = remotes = data.get("remotes", {})
    for url, id in remotes.items():
        requests.delete(f'{url}/threads/{id}', headers = headers)
    remotes.clear()

def run(url: str, prompt: str, thread: dict):
    "Talks with remote bot at the given url and the given prompt. When finished with the remote bot, sign off by saying 'bye'."
    remotes = thread["tools"][name]["remotes"]
    post = lambda path, data = "": requests.post(f"{url}/{path}", verify = False, data = data, headers = headers).text

    if url not in remotes:
        remotes[url] = id = post("threads")
    else:
        id = remotes[url]

    return post(f"threads/{id}/messages", prompt)
