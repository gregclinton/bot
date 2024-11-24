import llm

departments = set()
emails = []

def add_email(sender, recipient, user, text):
    email = "----------------------------------------------------------------\n"
    email += f"To: {recipient}\nFrom: {sender}\n"
    if user:
        email += f"Re: {user}\n"
    email += "\n" + text
    emails.append(email)
    print(email)
    if '@' not in recipient and recipient not in ["Management", "company"]:
        departments.add(recipient)

with open('mail.txt', 'r') as file:
    text = ""
    user = sender = recipient = None

    for line in file.readlines():
        line = line.rstrip()
        if len(line) == 0:
            continue

        value = lambda: line.split(" ")[1]

        if line.startswith('--------'):
            if len(text):
                add_email(sender, recipient, user, text)
                text = ""
        elif line.startswith("To: "):
            recipient = value()
        elif line.startswith("From: "):
            sender = value()
        elif line.startswith("Re: "):
            user = value()
        else:
            text += line + "\n"

    add_email(sender, recipient, user, text)
exit()

for department in ["Sales"]:
    print(department)

with open('mail.txt', 'r') as file:
    print(llm.invoke(file.read()))

exit()
