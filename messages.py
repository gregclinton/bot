import re, os

class Message:
    def __init__(self, from_, to_, body):
        self.from_ = from_
        self.to_ = to_
        self.body = body.strip()

    def to_string(self):
        text = "To: " + self.to_ + "\nFrom: " + self.from_ + "\n"
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
        to_, from_, user, body = ("", "", "", "")

        for line in cut.split("\n"):
            value = lambda: line.rstrip().split(" ")[1]

            if line.startswith("To: "):
                to_ = value()
            elif line.startswith("From: "):
                from_ = value()
            else:
                body += line + "\n"
        msg = Message(from_, to_, body)

        if keep(msg):
            msgs.append(msg)
    return msgs

path = lambda company, caller: f"messages/{company}/{caller}/messages.txt"

def load(company, caller, keep = lambda msg: True):
    file_path =path(company, caller)
    os.makedirs(os.path.dirname(file_path), exist_ok = True)

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return from_string(file.read(), keep)
    else:
        # create a small list of messages so llm get's the idea
        intake = "Intake"
        return [
            Message(caller, intake, "Where am I?"),
            Message(intake, caller, f"This is {company}."),
        ]

def save(company, caller, msgs):
    file_path =path(company, caller)
    os.makedirs(os.path.dirname(file_path), exist_ok = True)

    file_empty = not os.path.exists(file_path)
    with open(file_path, "a") as file:
        if not file_empty:
            file.write(perforation)
        file.write(to_string(msgs))

def delete_caller(company, caller):
    file_path =path(company, caller)

    if os.path.exists(file_path):
        os.remove(file_path)
