import messages
import time
import llm

def my_account_messages(me, account):
    for m in messages.mine(me):
        if (any(account in s for s in [m.text, m.to, m.poster]) or m.poster == "Chief"):
            yield m

while True:
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)
    account = "CX143623"

    me = "Hal"
    text = ""

    dashes = ""
    for msg in my_account_messages(me, account):
        text += f"{dashes}To: {msg.to}\nFrom: msg{msg.poster}\n{msg.text}\n"
        dashes = "------------------------------------------------------------\n"
        

    print(text)

    me = "Billing"
    text = ""

    dashes = ""
    for msg in my_account_messages(me, account):
        text += f"{msg.poster} to {msg.to}: {msg.text}\n"
        dashes = "------------------------------------------------------------\n"

    print(text)

    time.sleep(1)