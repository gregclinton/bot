# sh company run acme "What is my balance? And do you sell shoes?"

import llm
import messages
from messages import Message
import tool

name = "Switchboard"
next = ""

def invoke(caller, prompt):
    global name
    name = next or name
    company = name
    intake = "Intake"
    agents = set([intake])
    max_llm_invokes = 10
    llm.reset_counter()
    run = [Message(caller, intake, prompt)]
    history = messages.load(company, caller)

    while agents and llm.counter < max_llm_invokes:
        agent = agents.pop()
        instructions = open("instructions", "r").read() + open(f"ar/{company}/{agent}", "r").read()
        instructions = instructions.replace("{department}", agent).replace("{company}", company)
        instructions += "\nDon't forget to format your reply as a message with To: and From: fields.\n"
        msgs = list(filter(lambda msg: agent in (msg.from_, msg.to_), history + run))
        completion = llm.invoke(instructions, messages.to_string(msgs))

        for msg in messages.from_string(completion):
            run.append(msg)
            if msg.to_ in tool.bench:
                run.append(Message(msg.to_, msg.from_, tool.bench[msg.to_](msg.body)))
                agents.add(msg.from_)
            else:
                agents.add(msg.to_)

        if run[-1].to_ == caller:
            break

    if run[-1].to_ != caller:
        run += [Message(intake, caller, "Could you repeat that?")]

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
