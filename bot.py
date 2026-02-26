import messages
import time
import llm

while True:
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)
    account = "CX143623"

    me = "Hal"
    text = ""

    for msg in messages.mine(me, account):
        text += f"{msg.poster} to {msg.to}: {msg.text}\n"

    print(text)

    me = "Billing"
    text = ""

    for msg in messages.mine(me, account):
        text += f"{msg.poster} to {msg.to}: {msg.text}\n"

    print(text)

    time.sleep(1)