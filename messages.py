import re

class Email:
    def __init__(self, sender, recipient, body, user):
        self.sender = sender
        self.recipient = recipient
        self.body = body

        match = re.search(r'account-\d{6}', self.to_string())
        self.account = match.group() if match else None

    def to_string(self):
        text = "--------------------------------------------------------------------------------\n"
        text += "To: " + self.recipient + "\nFrom: " + self.sender + "\n"
        text += self.body
        return text.rstrip() + "\n"

    @staticmethod
    def from_string(text):
        recipient, sender, user, body = ("", "", "", "")

        for line in text.split("\n"):
            value = lambda: line.rstrip().split(" ")[1]

            if line.startswith("To: "):
                recipient = value()
            elif line.startswith("From: "):
                sender = value()
            else:
                body += line + "\n"
        return Email(sender, recipient, body, user)
