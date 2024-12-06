import requests

def invoke(text, thread):
    url, prompt = text.split("\n")
    headers = { "Content-Type": "text/plain" }
    post = lambda path, data = "": requests.post(f"{url}/{path}", data = data, headers = headers).text

    url = url.strip()
    if url not in thread["bots"]:
        thread["bots"][url] = id = post("threads")
    else:
        id = thread["bots"][url]

    return post(f"threads/{id}/messages", prompt)