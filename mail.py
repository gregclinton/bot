import llm

departments = set()
emails = []

def add_email(sender, recipient, user, body):
    email = "----------------------------------------------------------------\n"
    email += f"To: {recipient}\nFrom: {sender}\n"
    if user:
        email += f"Re: {user}\n"
    email += "\n" + body
    emails.append(email)
    print(to_string(email))
    if '@' not in recipient and recipient not in ["Management", "company"]:
        departments.add(recipient)

def to_string(email):
    text = "----------------------------------------------------------------\n"
    text += "To: " + email["recipient"] + "\nFrom: " + email["sender"] + "\n"
    if "user" in email:
        test += "Re: " + email["user"] + "\n"
    text += body
 
with open('mail.txt', 'r') as file:
    email = {}
    body = ""

    for line in file.readlines():
        value = lambda: line.split(" ")[1]

        if line.startswith('--------'):
            if len(body):
                email["body"] = body
                emails.append(email)
                body = ""
        elif line.startswith("To: "):
            email["recipient"] = value()
        elif line.startswith("From: "):
            email["sender"] = value()
        elif line.startswith("Re: "):
            email["user"] = value()
        else:
            body += line
    emails.append(email)

for department in ["Sales"]:
    for email in emails:
        if email["recipient"] in [department, "company"]:
            print(to_string(email))
            continue
        
            with open('mail.txt', 'r') as file:
                print(llm.invoke(to_string(email)))