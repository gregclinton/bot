import messages
import llm
import re

workers = []

for msg in messages.archive("Chief"):
    if msg.to not in ["Chief", "Shell"] + workers:
        workers.append(msg.to)

def post(worker, text):
    for part in re.split(r'\n-{4,}\n', text.strip()):
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        if len(lines) > 2 and lines[0].startswith('To:') and lines[1].startswith('From:'):
            to = lines[0].split(':',1)[1].strip()
            frm = lines[1].split(':',1)[1].strip()
            if frm == worker:
                print('\n'.join(lines), '\n\n')
                messages.post(to, frm, "\n".join(lines[2:]))

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
            post(worker, llm.invoke("groq", "openai/gpt-oss-20b", "", text))
