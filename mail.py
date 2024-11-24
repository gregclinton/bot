import llm

departments = set()
emails = []

def to_string(email):
    text = "----------------------------------------------------------------\n"
    text += "To: " + email["recipient"] + "\nFrom: " + email["sender"] + "\n"
    if "user" in email:
        test += "Re: " + email["user"] + "\n"
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
        elif not line.startswith('--------'):
            body += line

    email["body"] = body
    return email

with open('mail.txt', 'r') as file:
    text = ""

    for line in file.readlines():
        if line.startswith('--------'):
            if len(text):
                emails.append(parse(text))
                text = ""
        text += line

    emails.append(parse(text))

for department in ["Sales"]:
    instuction = f"You are an AI worker in {department}. Take care of emails addressed to you."
    prompt = ""
    for email in emails:
        if email["recipient"] in [department, "company"]:
            prompt += to_string(email)

    if True:
        with open('mail.txt', 'r') as file:
            print(llm.invoke(instuction, prompt))