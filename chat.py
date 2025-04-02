import llm
import tool
import os
import httpx
from fastapi import UploadFile

def reset(thread):
    spec = open(f"assistants/{thread['assistant']}").read().split("\n")
    tokens = spec[0].split(' ')
    thread["provider"] = tokens[0]
    model = tokens[1]
    tools = tokens[2:]
    content = "\n".join(spec[1:])
    thread["model"] = model
    thread["tools"] = tool.create(tools)
    tool.reset(tools, thread)
    thread["messages"] = [
        { "role": "user", "content": content},
        { "role": "assistant", "content": "Yes, proceed."}
    ]
    thread["runs"] = []
    return thread

def back(thread):
    del thread["messages"][thread["runs"].pop():]

async def run(prompt, thread):
    def message(role, content):
        if role == "user":
            print(f"{thread['user']} to {thread['assistant']}:")
        elif role == "assistant":
            print(f"{thread['assistant']} to {thread['user']}:")
        print(f"{content}\n", flush=True)
        return { "role": role, "content": content }

    messages = thread["messages"]
    thread["runs"].append(len(thread["messages"]))
    messages.append(message("user", prompt))
    reply = await llm.invoke(thread)
    messages.append(message("assistant", reply))
    return reply

def set_model(thread, provider, model):
    thread["provider"] = provider
    thread["model"] = model
    for message in thread["messages"]:
        if message["role"] == "assistant":
            for key in ["refusal", "annotations"]:
                message.pop(key, None)

async def transcribe(thread, file: UploadFile):
    async with httpx.AsyncClient(timeout = 60) as client:
        transcription = (await client.post(
            url = f"https://api.groq.com/openai/v1/audio/transcriptions",
            headers = { "Authorization": "Bearer " + os.environ.get("GROQ_API_KEY") },
            files = { "file": (file.filename, await file.read(), file.content_type) },
            data = {
                "model": "whisper-large-v3-turbo",
                "response_format": "text"
            }
        )).text

        context = "\n".join(msg.get("content", "") for msg in thread["messages"])

        return (await client.post(
            url = "https://api.openai.com/v1/chat/completions",
            headers = {
                'Authorization': 'Bearer ' + os.environ.get("OPENAI_API_KEY"),
                'Content-Type': 'application/json'
            },
            json = {
                "model": "gpt-4o-mini",
                "temperature": 0,
                "messages": [
                    {
                        "role": "system",
                        "content": "Use the provided context to make any needed corrections to the provided speech-to-text transcription. Output your raw fix."
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nTranscription:\n{transcription}\n\nReturn the transcription with your fixes."
                    }
                ]
            }
        )).json()["choices"][0]["message"]["content"]
