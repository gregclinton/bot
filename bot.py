import messages
import llm
import re
import subprocess

workers = []

for msg in messages.archive("Chief"):
    if msg.to not in (["Chief", "Shell"] + workers):
        workers.append(msg.to)

def post(worker, text):
    for part in re.split(r'\n-{4,}\n', text.strip()):
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        if len(lines) > 2 and lines[0].startswith('From:') and lines[1].startswith('To:'):
            frm = lines[0].split(':',1)[1].strip()
            to = lines[1].split(':',1)[1].strip()
            body = "\n".join(lines[2:])
            if frm == worker:
                print(f"From: {frm}\nTo: {to}\n{body}\n")
                messages.post(frm, to, body)

for msg in messages.inbox("Shell"):
    p = subprocess.run(msg.body, shell = True, capture_output = True, text = True)
    results = p.stdout + p.stderr
    messages.post("Shell", msg.poster, f"Your bash shell command:\n{msg.body}\n\nProduced these results:\n{results}")

for worker in workers:
    accounts = set()

    for msg in messages.inbox(worker):
        m = re.search(r"\bCX1\w*", f"{msg.poster} {msg.body}")
        if m:
            accounts.add(m.group())

    for account in accounts:
        text = ""
        dashes = ""
        for msg in messages.archive(worker):
            if (any(account in s for s in [msg.body, msg.to, msg.poster]) or msg.poster == "Chief"):
                t = msg.time.strftime("%A, %B %-d, %-I:%M %P")
                text += f"{dashes}{t}\nFrom: {msg.poster}\nTo: {msg.to}\n{msg.body}\n"
                dashes = "----------------------------\n"

        if text != "":
            post(worker, llm.invoke("groq", "openai/gpt-oss-20b", "", text).strip())