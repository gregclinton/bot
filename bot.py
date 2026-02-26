import messages
import time
import llm

def run_worker(worker, account):
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)
    text = ""

    dashes = ""
    for msg in messages.mine(worker):
        if (any(account in s for s in [msg.text, msg.to, msg.poster]) or msg.poster == "Chief"):
            text += f"{dashes}To: {msg.to}\nFrom: msg{msg.poster}\n{msg.text}\n"
            dashes = "------------------------------------------------------------\n"
        
    print(invoke("", text))

while True:
    account = "CX143623"
    run_worker("Hal", account)
    run_worker("Billing", account)
    time.sleep(10)