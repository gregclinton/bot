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
    instruction = f"You are an AI worker in {department}. "
    instruction += "Take care of emails to you only if they require a reply. "
    instruction += "The emails are shown in chronological order. "
    prompt = ""
    last_email = None

    # get last email to this department
    for email in emails:
        if email["recipient"] == department:
            last_email = email

    if not last_email:
        return

    is_email = lambda s : "@" in s
    user = email["sender"] if is_email(email["sender"]) else email["user"] if "user" in email else None

    # include unanswered emails to this department
    # for each unanswered email include all emails with same user
    # and always include emails to company
    # and always include emails from Management to this department
    for email in emails:
        if email["recipient"] in [department, "company"]:
            prompt += to_string(email)

    with open('mail.txt', 'r') as file:
        for cut in split_cuts(llm.invoke(instruction, prompt)):
            print(to_string(parse(cut)))