import telegram
import sys
import messages

def run(worker, scissors, post, text):
    frm = to = body = ""

    for line in text.splitlines():
        if line.startswith("From:"):
            frm = line.split(':')[1].strip()
        elif line.startswith("To:"):
            to = line.split(':')[1].strip()
        elif line.startswith(scissors):
            post(worker, frm, to, body)
            frm = to = body = ""
        else:
            body += f"{line}\n"

    if post:
        post(worker, frm, to, body)
    else:
        messages.post(frm, to, body)

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])