import llm

class Email:
    def __init__(self, sender, recipient, body, user):
        self.sender = sender
        self.recipient = recipient
        self.user = user
        self.body = body

    def to_string(self):
        text = "--------------------------------------------------------------------------------\n"
        text += "To: " + self.recipient + "\nFrom: " + self.sender + "\n"
        if self.user:
            text += "Re: " + self.user + "\n"
        text += self.body
        return text

    @staticmethod
    def from_string(text):
        recipient, sender, user, body = ("", "", "", "")

        for line in text.split("\n"):
            value = lambda: line.rstrip().split(" ")[1]

            if line.startswith("To: "):
                recipient = value()
            elif line.startswith("From: "):
                sender = value()
            elif line.startswith("Re: "):
                user = value()
            else:
                body += line + "\n"
        return Email(sender, recipient, body, user)

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

departments = set()
emails = []

with open('mail.txt', 'r') as file:
    for cut in split_cuts(file.read()):
        email = Email.from_string(cut)
        if email.sender == "Management" and email.recipient != "company":
            departments.add(email.recipient)
        emails.append(email)

for department in departments:
    instruction = f"You are an AI worker in {department}. "
    instruction += "Take care of emails to you only if they require a reply. "

    instruction += "The emails are shown in chronological order. "
    user = None

    for email in emails:
        if email.recipient == department:
            user = email.user

    if not user:
        continue

    prompt = ""

    for email in emails:
        come_from_above = lambda: email.sender in ["Management"]
        visible_to_us = lambda: email.recipient in [department, "company"]
        to_or_from_us = lambda: email.recipient == department or email.sender == department
        re_the_user = lambda: email.user == user

        if (come_from_above() and visible_to_us()) or (re_the_user() and to_or_from_us()):
            prompt += email.to_string()

    with open('mail.txt', 'r') as file:
        for cut in split_cuts(llm.invoke(instruction, prompt)):
            print(Email.from_string(cut).to_string())