# sh company run sephora "Do you sell men's shoes?"
# sh company run sephora "What's my balance?"

import llm
import messages
from messages import Message
import tools

company = "sephora"

def invoke(caller, prompt):
    messages.company = company
    intake = "Intake"
    agents = set()
    max_llm_invokes = 10
    llm.reset_counter()
    run = [Message(caller, intake, prompt)]
    history = messages.load(lambda msg: msg.caller == caller)

    agents.add(intake)

    while llm.counter < max_llm_invokes and agents:
        agent = agents.pop()
        read = lambda path: open(f"ar/{company}/{path}", "r").read()
        instructions = read("All").replace("{agent}", agent) + read(agent)

        if agent in tools.bench:
            run += messages.from_string(tools.invoke(agent, run))
            agents.add(run[-1].to_)
        else:
            msgs = list(filter(lambda msg: agent in (msg.from_, msg.to_), history)) + run
            completion = llm.invoke(instructions, messages.to_string(msgs))
            sanity = lambda msg: msg.from_ == agent and msg.to_ != msg.from_ and (msg.to_ != caller or msg.from_ == intake)
            msgs = messages.from_string(completion, sanity)
            agents.update(msg.to_ for msg in msgs if msg.to_ != caller)
            run += msgs

        if run[-1].to_ == caller:
            break

    if run[-1].to_ != caller:
        run += [Message(intake, caller, "Could you repeat that?")]

    print(messages.to_string(run))
    messages.save(run)
    return run[-1].body

import sys

if __name__ == "__main__":
    company = sys.argv[2]
    prompt = sys.argv[3]
    invoke("account-375491", prompt)
