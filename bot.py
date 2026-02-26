import messages
import time
import llm

while True:
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)

    me = "Hal"
    account = "CX143623"
    text = ""

    for msg in filter(lambda msg: any(account in s for s in [msg.text, msg.to, msg.poster]) or msg.poster == "Chief",  messages.mine(me)):
        text += f"{msg.poster} to {msg.to}: {msg.text}\n"

    print(text)

    me = "Billing"
    account = "CX143623"
    text = ""

    for msg in filter(lambda msg: any(account in s for s in [msg.text, msg.to, msg.poster]) or msg.poster == "Chief",  messages.mine(me)):
        text += f"{msg.poster} to {msg.to}: {msg.text}\n"

    print(text)

    time.sleep(1)