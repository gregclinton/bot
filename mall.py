# sh mall run acme "What is my balance? And do you sell shoes?"

import llm
import messages
from messages import Message
import tool

name = "The Mall"
next = ""

def invoke(caller, prompt):
    company = next or name
    intake = "Intake"
    departments = {intake}
    max_llm_invokes = 10
    llm.reset_counter()
    run = [Message(caller, intake, prompt)]
    history = messages.load(company, caller)

    while departments and llm.counter < max_llm_invokes:
        department = departments.pop()
        instructions = "".join(open(f, "r").read() for f in ["instructions", f"ar/{company}/{department}"])
        instructions = instructions.format_map({"company": company, "department": department, "caller": caller})

        msgs = list(filter(lambda msg: department in (msg.from_, msg.to_), history + run))
        prompt = "Complete the email thread:\n" + messages.to_string(msgs) + messages.perforation
        completion = llm.invoke(instructions, prompt)

        for msg in messages.from_string(completion):
            run.append(msg)
            if msg.to_ in tool.bench:
                body = tool.bench[msg.to_](company, department, caller, msg.body) if (lambda: True)() else str(e)
                run.append(Message(msg.to_, msg.from_, body))
                departments.add(msg.from_)
            else:
                departments.add(msg.to_)

        if run[-1].to_ == caller:
            break

    if run[-1].to_ != caller:
        run += [Message(intake, caller, "I got an error because I forgot to use To: and From: in my response. I'm going to try again. Okay?")]

    print(messages.to_string(run))
    messages.save(company, caller, run)

    return {
        "company": next or name,
        "content": run[-1].body
    }

import sys

if __name__ == "__main__":
    name = sys.argv[2]
    prompt = sys.argv[3]
    invoke("account-375491", prompt)
