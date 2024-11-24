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
 
with open('mail.txt', 'r') as file:
    email = {}
    body = ""

    for line in file.readlines():
        value = lambda: line.rstrip().split(" ")[1]

        if line.startswith('--------'):
            if len(body):
                email["body"] = body
                emails.append(email)
                email = {}
                body = ""
        elif line.startswith("To: "):
            email["recipient"] = value()
        elif line.startswith("From: "):
            email["sender"] = value()
        elif line.startswith("Re: "):
            email["user"] = value()
        else:
            body += line

    email["body"] = body
    emails.append(email)

for department in ["Sales"]:
    text = ""
    for email in emails:
        if email["recipient"] in [department, "company"]:
            text += to_string(email)

    if True:
        with open('mail.txt', 'r') as file:
            print(llm.invoke(text))