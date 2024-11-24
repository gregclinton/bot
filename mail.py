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
    print(email)
    if '@' not in recipient and recipient not in ["Management", "company"]:
        departments.add(recipient)
 
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
            print(email)
        elif line.startswith("To: "):
            email["recipient"] = value()
        elif line.startswith("From: "):
            email["sender"] = value()
        elif line.startswith("Re: "):
            email["user"] = value()
        else:
            body += line

    emails.append(email)
exit()

for department in ["Sales"]:
    print(department)

with open('mail.txt', 'r') as file:
    print(llm.invoke(file.read()))

exit()
