import catalog
import messages
from messages import Message

bench = {
    "Catalog": catalog.invoke
}

def invoke(tool, msgs):
    lookup = set()
    unanswered = []
    answers = []
    fn = bench[tool]

    for msg in msgs:
        if msg.recipient == tool:
            unanswered.append(msg)

    for msg in unanswered:
        answers.append(Message(tool, msg.sender, fn(msg.body)))

    return messages.to_string(answers) if answers else ""
