import llm
import catalog
import messages
from messages import Message

counter = 0
def call_tool(tool, text):
    if tool == "Catalog":
        context = catalog.query(text)
        return llm.invoke("Based on the context, provide the answer to the question.", f"Context: {context}\nQuestion: {text}\nAnswer: ")

    return "???"

def invoke(tool, msgs):
    print(messages.to_string(msgs))
    exit()
    global counter
    if counter > 0 or msgs[0].sender != "Sales":
        return ""
        
    counter += 1


    return messages.to_string([Message(tool, msgs[0].sender, "Sorry, it is not in our catalog.")])
    # First determine which tool msgs have not been answered.
    # Then for these, print out completion string consisting of tool answers with To: msg.sender From: tool and body answer
    unanswered = []
    answers = []

    for msg in msgs:
        if msg.recipient == tool:
            unanswered.append(msg)
            break

    for msg in unanswered:
        answers.append(Message(tool, msg.sender, call_tool(tool, msg.body)))

    return messages.to_string(answers) if answers else ""

