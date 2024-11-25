import re

class Message:
    def __init__(self, sender, recipient, body, user):
        self.sender = sender
        self.recipient = recipient
        self.body = body

        match = re.search(r'account-\d{6}', self.to_string())
        self.account = match.group() if match else None

    def to_string(self):
        text = "To: " + self.recipient + "\nFrom: " + self.sender + "\n"
        text += self.body.rstrip() + "\n"
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
            else:
                body += line + "\n"
        return Message(sender, recipient, body, user)

class Messages:
    perforation = "----------------------------------------------------------------------\n"

    @staticmethod
    def to_string(msgs):
        return Messages.perforation.join(map(lambda msg: msg.to_string(), msgs))

    @staticmethod
    def from_string(text, condition = None):
        msgs = []

        # replace hyphens in text to match perforation

        for cut in text.split(Messages.perforation):
            msg = Message.from_string(cut)
            if not condition or condition(msg):
                msgs.append(msg)
        return msgs

    @staticmethod
    def save(msgs):
        with open(msgs, 'w') as file:
            file.write(Messages.to_string(msgs))

    @staticmethod
    def load(path, condition = None):
        with open(path, 'r') as file:
            return Messages.from_string(file.read(), condition)

    @staticmethod
    def recipients(path, condition = None):
        recipients = set()

        for msg in Messages.load(path, condition):
            recipients.add(msg.recipient)

        return list(recipients)
