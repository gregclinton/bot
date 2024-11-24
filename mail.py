import llm

departments = set()
emails = []

def to_string(email):
    text = "--------------------------------------------------------------------------------\n"
    text += ("To: " + email["recipient"] + "\nFrom: " + email["sender"] + "\n")
    if "user" in email:
        text += ("Re: " + email["user"] + "\n")
    text += email["body"]
    return text

def parse(text):
    email = {}
    body = ""

    for line in text.split("\n"):
        value = lambda: line.rstrip().split(" ")[1]

        if line.startswith("To: "):
            email["recipient"] = value()
        elif line.startswith("From: "):
            email["sender"] = value()
        elif line.startswith("Re: "):
            email["user"] = value()
        else:
            body += line + "\n"

    email["body"] = body
    return email

def split_cuts(text):
    cuts = []
    cut = ""

    for line in text.split("\n"):
        if line.startswith('--------'):
            if len(cut):
                cuts.append(cut)
                cut = ""
        else:
            cut += line + "\n"

    if len(cut):
        cuts.append(cut)

    return cuts

with open('mail.txt', 'r') as file:
    for cut in split_cuts(file.read()):
        emails.append(parse(cut))

for department in ["Sales"]:
    instuction = f"You are an AI worker in {department}. Take care of emails to you only if they require a reply. "
    prompt = ""

    for email in emails:
        if email["recipient"] in [department, "company"]:
            prompt += to_string(email)

    with open('mail.txt', 'r') as file:
        for cut in split_cuts(llm.invoke(instuction, prompt)):
            print(to_string(parse(cut)))