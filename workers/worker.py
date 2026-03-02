# python3 workers/worker.py run groq openai/gpt-oss-120b Above Hal

import llm
import re
import storage
import sys
import messages

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

def run(llm_provider, llm_model, chief, worker):
    accounts = storage.root / "workers" / worker
    accounts.mkdir(parents = True, exist_ok = True)

    for msg in messages.inbox(worker):
        if msg.frm == chief:
            afasfdsaf
        else:
            m = re.search(r"\bCX1\w*", f"{msg.frm} {msg.body}")
            if m:
                account = m.group()
                (accounts / account).append_text(msg.body)
    return

    for account in accounts:
        text = ""
        dashes = ""
        for msg in messages.archive(worker):
            if (any(account in s for s in [msg.body, msg.to, msg.frm]) or msg.frm == chief):
                t = msg.time.strftime("%A, %B %-d, %-I:%M %P")
                text += f"{dashes}{t}\nFrom: {msg.frm}\nTo: {msg.to}\n{msg.body}\n"
                dashes = "----------------------------\n"

        if text != "":
            post(worker, llm.invoke(llm_provider, llm_model, "", text).strip())

if __name__ == "__main__":
    name = sys.argv[1]
    args = sys.argv[2:]
    {"run": run}[name](*args)