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

perforation = "\n------------------------------------------------------------\n"

def fix_perforations(s):
    return re.sub(r"^-{3,}$", "-" * 60, s, flags=re.MULTILINE)

def to_string(msgs):
    return perforation.join(map(lambda msg: msg.to_string(), msgs))

def from_string(text, keep = lambda msg: True):
    msgs = []

    for cut in fix_perforations(text).split(perforation):
        recipient, sender, user, body = ("", "", "", "")

        for line in cut.split("\n"):
            value = lambda: line.rstrip().split(" ")[1]

            if line.startswith("To: "):
                recipient = value()
            elif line.startswith("From: "):
                sender = value()
            else:
                body += line + "\n"
        msg = Message(sender, recipient, body)

        if keep(msg):
            msgs.append(msg)
    return msgs

def load(path, keep = lambda msg: True):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return from_string(file.read(), keep)
    return []

def recipients(path, keep = lambda msg: True):
    recipients = set()

    for msg in load(path, keep):
        recipients.add(msg.recipient)

    return recipients

def append_to_file(path, msgs):
    text = to_string(msgs)
    file_empty = not os.path.exists(path)
    with open(path, "a") as file:
        if not file_empty:
            file.write(perforation)
        file.write(text)
