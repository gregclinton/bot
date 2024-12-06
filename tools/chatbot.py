import requests

def invoke(text, thread):
    url, prompt = text.split("\n")
    headers = { "Content-Type": "application/json" }
    post = lambda path, data = {}: requests.post(f"{url}/{path}", json = data, headers = headers).json()

    if url not in thread["bots"]:
        thread["bots"][url] = id = post("threads")["id"]
    else:
        id = thread["bots"][url]

    return post(f"threads/{id}/messages", {
        "role": "user",
        "content": prompt
    })["content"]
