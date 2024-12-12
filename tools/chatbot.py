import requests

def restart(thread):
    me = thread["tools"].get("chatbot", {})
    me["bots"] = bots = me.get("bots", {})
    for url, id in bots.items():
        requests.delete(f'{url}/threads/{id}', headers={ 'Content-Type': 'text/plain' })
    bots.clear()

def meta():
    return {
        "description": "Talk with another chatbot.",
        "parameters": {
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The other chatbot's url."
                },
                "prompt": {
                    "type": "string",
                    "description": "Your prompt to the other chatbot."
                }
            },
            "required": ["url", "prompt"]
        }
    }

def run(args, thread):
    url = args["url"]
    me = thread["tools"]["chatbot"]
    headers = { "Content-Type": "text/plain" }
    post = lambda path, data = "": requests.post(f"{url}/{path}", data = data, headers = headers).text

    if url not in me["bots"]:
        me["bots"][url] = id = post("threads")
    else:
        id = me["bots"][url]

    return post(f"threads/{id}/messages", args["prompt"])