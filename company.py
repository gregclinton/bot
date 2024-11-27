import llm
import messages
from messages import Message
import tools

def invoke(caller, prompt):
    company = "sephora"
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
        else:
            msgs = list(filter(lambda msg: agent in (msg.from_, msg.recipient), history)) + run
            completion = llm.invoke(instructions, messages.to_string(msgs))
            sanity = lambda msg: msg.from_ == agent and msg.recipient != msg.from_ and (msg.recipient != caller or msg.from_ == intake)
            msgs = messages.from_string(completion, sanity)
            for msg in msgs:
                if msg.recipient != caller:
                    agents.add(msg.recipient)
            run += msgs

        if run[-1].recipient == caller:
            break

    if run[-1].recipient != caller:
        run += [Message(intake, caller, "Could you repeat that?")]

    print(messages.to_string(run))
    messages.save(run)
    return run[-1].body

# invoke("account-375491", "Do you sell men's shoes?")
invoke("account-375491", "What's my balance?")
