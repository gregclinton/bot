import messages
import time
import llm
import re

def post(text):
    for part in re.split(r'\n-{4,}\n', text.strip()):
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        if len(lines) < 3 or ':' not in lines[0] or ':' not in lines[1]:
            continue
        if not lines[0].lower().startswith('to:') or not lines[1].lower().startswith('from:'):
            continue
        print('\n'.join(lines), '\n-----------------------------');
        messages.post(lines[0].split(':',1)[1].strip(),
             lines[1].split(':',1)[1].strip(),
             "\n".join(lines[2:]))

def run_worker(worker, account):
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)
    text = ""

    dashes = ""
    for msg in messages.mine(worker):
        if (any(account in s for s in [msg.text, msg.to, msg.poster]) or msg.poster == "Chief"):
            text += f"{dashes}To: {msg.to}\nFrom: {msg.poster}\n{msg.text}\n"
            dashes = "----------------------------\n"
        
    post(invoke("", text))

while True:
    account = "CX143623"
    run_worker("Hal", account)
    run_worker("Billing", account)
    time.sleep(10)