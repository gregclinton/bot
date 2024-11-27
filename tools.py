import catalog
import messages
from messages import Message

bench = {
    "Catalog": catalog.invoke
}

def invoke(tool, msgs):
    count = 0

    for msg in msgs:
        if msg.from_ == tool:
            count += 1

    answers = []
    fn = bench[tool]
    for msg in msgs:
        if msg.to_ == tool:
            if count == 0:
                answers.append(Message(tool, msg.from_, fn(msg.body)))
            else:
                count -= 1

    return answers
