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

departments = set()
emails = []

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
        emails.append(Email.from_string(cut))

for department in ["Sales"]:
    instruction = f"You are an AI worker in {department}. "
    instruction += "Take care of emails to you only if they require a reply. "

    instruction += "The emails are shown in chronological order. "
    last_email = None

    # get last email to this department
    for email in emails:
        if email.recipient == department:
            last_email = email

#    if not last_email:
#        continue

    # include unanswered emails to this department
    # for each unanswered email include all emails with same user
    # and always include emails to company
    # and always include emails from Management to this department
    prompt = ""

    for email in emails:
        if email.recipient in [department, "company"]:
            prompt += email.to_string()

    with open('mail.txt', 'r') as file:
        for cut in split_cuts(llm.invoke(instruction, prompt)):
            print(Email.from_string(cut).to_string())