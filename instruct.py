def post(worker, frm, to, body):
    if frm == worker and to and body:
        body = body.strip()
        (accounts / account / f"{last_timestamp + 1}|{frm}|{to}").write_text(body)

        if to.startswith("TLG") or frm.startswith("TLG"):
            print(f"From: {frm}\nTo: {to}\n{body}\n==========================", flush = True)

        if to.startswith("TLG"):
            if frm == "Hal":
                telegram.post(to[3:], body)
        else:
            messages.post(frm, to, body)

def run(text)
    frm = to = body = ""

    for line in text.splitlines():
        if line.startswith("From:"):
            frm = line.split(':')[1].strip()
        elif line.startswith("To:"):
            to = line.split(':')[1].strip()
        elif line.startswith("---"):
            post(worker, frm, to, body)
            frm = to = body = ""
        else:
            body += f"{line}\n"

    post(worker, frm, to, body)