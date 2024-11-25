import re, os

class Message:
    def __init__(self, sender, recipient, body):
        self.sender = sender
        self.recipient = recipient
        self.body = body.strip()

        match = re.search(r'account-\d{6}', self.to_string())
        self.account = match.group() if match else None

    def to_string(self):
        text = "To: " + self.recipient + "\nFrom: " + self.sender + "\n"
        text += self.body.strip()
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
        return Message(sender, recipient, body)

class Messages:
    perforation = "\n------------------------------------------------------------\n"

    @staticmethod
    def fix_perforations(s):
        return re.sub(r"^-{3,}$", "-" * 60, s, flags=re.MULTILINE)

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
        if os.path.exists(path):
            with open(path, 'r') as file:
                return Messages.from_string(file.read(), keep)
        return []

    @staticmethod
    def recipients(path, keep = lambda msg: True):
        recipients = set()

        for msg in Messages.load(path, keep):
            recipients.add(msg.recipient)

        return list(recipients)

    @staticmethod
    def append_string_to_file(path, text):
        if len(path) > 0:
            file_empty = not os.path.exists(path)
            with open(path, "a") as file:
                if not file_empty:
                    file.write(Messages.perforation)
                file.write(text.rstrip())
