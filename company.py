import llm
import messages
from messages import Message, load
import tools

def invoke(caller, prompt):
    company = "sephora"
    intake = "Intake"
    agents = set()
    max_llm_invokes = 10
    llm.reset_counter()
    run = [Message(caller, intake, prompt)]
    history = load(lambda msg: msg.caller == caller)

    agents.add(intake)

    while llm.counter < max_llm_invokes and agents:
        agent = agents.pop()
        read = lambda path: open(f"ar/{company}/{path}", "r").read()
        instructions = read("All").replace("{agent}", agent) + read(agent)

        if agent in tools.bench:
            msgs = messages.from_string(tools.invoke(agent, run))
        else:
            msgs = list(filter(lambda msg: agent in (msg.from_, msg.recipient), history)) + run
            completion = llm.invoke(instructions, messages.to_string(msgs))
            sanity = lambda msg: msg.from_ == agent and msg.recipient != msg.from_ and (msg.recipient != caller or msg.from_ == intake)
            msgs = messages.from_string(completion, sanity)

        run += msgs

        print(messages.to_string(msgs))
        print("--------------------------------------------")

        if len(msgs) == 1 and agent == intake:
            msg = msgs[0]
            if msg.recipient == caller:
                messages.save(run)
                return msg.body
            else:
                agents.add(msg.recipient)
        elif msgs:
            for msg in msgs:
                if msg.recipient != caller:
                    agents.add(msg.recipient)

    run += [Message(intake, caller, "Could you repeat that?")]
    messages.save(run)
    return run[-1].body

# invoke("account-375491", "Do you sell men's shoes?")
invoke("account-375491", "What's my balance?")
