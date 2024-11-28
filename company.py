# sh company run acme "What is my balance? And do you sell shoes?"

import llm
import messages
from messages import Message
import tool

def invoke(company, caller, prompt):
    intake = "Intake"
    agents = set([intake])
    max_llm_invokes = 10
    llm.reset_counter()
    run = [Message(caller, intake, prompt)]
    history = messages.load(company, caller)

    while agents and llm.counter < max_llm_invokes:
        agent = agents.pop()
        read = lambda path: open(f"ar/{company}/{path}", "r").read()
        instructions = read("All").replace("{agent}", agent) + read(agent)
        msgs = list(filter(lambda msg: agent in (msg.from_, msg.to_), history + run))
        completion = llm.invoke(instructions, messages.to_string(msgs))
        sanity = lambda msg: msg.from_ == agent and msg.to_ != msg.from_ and (msg.to_ != caller or msg.from_ == intake)

        for msg in messages.from_string(completion, sanity):
            run.append(msg)
            if msg.to_ in tool.bench:
                run.append(Message(msg.to_, msg.from_, tool.bench[msg.to_](msg.body)))
            else:
                agents.add(msg.to_)

        if run[-1].to_ == caller:
            break

    if run[-1].to_ != caller:
        run += [Message(intake, caller, "Could you repeat that?")]

    print(messages.to_string(run))
    messages.save(company, caller, run)
    return run[-1].body

import sys

if __name__ == "__main__":
    company = sys.argv[2]
    prompt = sys.argv[3]
    invoke(company, "account-375491", prompt)
