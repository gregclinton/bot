import messages
import time
import llm
import re

def post(worker, text):
    for part in re.split(r'\n-{4,}\n', text.strip()):
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        if len(lines) > 2 and lines[0].startswith('To:') and lines[1].startswith('From:'):
            to = lines[0].split(':',1)[1].strip()
            frm = lines[1].split(':',1)[1].strip()
            if frm == worker:
                print('\n'.join(lines), '\n\n')
                messages.post(to, frm, "\n".join(lines[2:]))

while True:
    account = "CX143623"
    for worker in ["Hal", "Billing"]:
        text = ""
        dashes = ""
        for msg in messages.mine(worker):
            if (any(account in s for s in [msg.text, msg.to, msg.poster]) or msg.poster == "Chief"):
                t = msg.time.strftime("%A, %B %-d, %-I:%M %P")
                text += f"{dashes}{t}\nTo: {msg.to}\nFrom: {msg.poster}\n{msg.text}\n"
                dashes = "----------------------------\n"

        post(worker, llm.invoke("groq", "openai/gpt-oss-20b", "", text))

    time.sleep(1)