import llm
import catalog
import messages
from messages import Message

def call_tool(tool, text):
    if tool == "Catalog":
        context = "A search of our product catalog yielded: \n" + catalog.query(text)
        instructions = "Provide the answer to the question given the context."
        prompt = f"Context: {context}\nQuestion: {question}\nAnswer: "
        return llm.invoke(instructions, prompt)
    else:
        return "???"

def invoke(tool, msgs):
    print(messages.to_string(msgs))

    lookup = set()
    unanswered = []
    answers = []

    for msg in msgs:
        if msg.recipient == tool:
            unanswered.append(msg)

    for msg in unanswered:
        answers.append(Message(tool, msg.sender, call_tool(tool, msg.body)))

    return messages.to_string(answers) if answers else ""

