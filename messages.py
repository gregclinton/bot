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
    perforation = "------------------------------------------------------------\n"

    @staticmethod
    def fix_perforations(s):
        return re.sub(r"^-{10,}$", "-" * 60, s, flags=re.MULTILINE)

    @staticmethod
    def to_string(msgs):
        return Messages.perforation.join(map(lambda msg: msg.to_string(), msgs))

    @staticmethod
    def from_string(text, keep = lambda msg: True):
        msgs = []

        for cut in Messages.fix_perforations(text).split(Messages.perforation):
            msg = Message.from_string(cut)
            if not keep or keep(msg):
                msgs.append(msg)
        return msgs

    @staticmethod
    def load(path, keep = lambda msg: True):
        with open(path, 'r') as file:
            return Messages.from_string(file.read(), keep)

    @staticmethod
    def recipients(path, keep = lambda msg: True):
        recipients = set()

        for msg in Messages.load(path, keep):
            recipients.add(msg.recipient)

        return list(recipients)
