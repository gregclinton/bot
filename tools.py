import catalog
import messages
from messages import Message

def invoke(tool, msgs):
    lookup = set()
    unanswered = []
    answers = []

    for msg in msgs:
        if msg.recipient == tool:
            unanswered.append(msg)

    for msg in unanswered:
        fn = catalog.invoke if tool == "Catalog" else lambda x: ""
        answers.append(Message(tool, msg.sender, fn(msg.body)))
    exit()

    return messages.to_string(answers) if answers else ""
