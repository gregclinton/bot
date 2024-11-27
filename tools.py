import catalog
import messages
from messages import Message

tools = {
    "Catalog": catalog.invoke
}

def invoke(tool, msgs):
    lookup = set()
    unanswered = []
    answers = []

    for msg in msgs:
        if msg.recipient == tool:
            unanswered.append(msg)

    for msg in unanswered:
        if tool in tools:
            answers.append(Message(tool, msg.sender, tools[tool](msg.body)))
    exit()

    return messages.to_string(answers) if answers else ""
