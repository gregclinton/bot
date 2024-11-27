import llm
import messages
from messages import Message, load
import tools

def invoke(account, prompt):
    company = "sephora"
    intake = "Intake"
    agents = set()
    max_llm_invokes = 10
    llm.reset_counter()
    run = [Message(account, intake, prompt)]
    history = load(lambda msg: msg.account == account)

    agents.add(intake)

    while llm.counter < max_llm_invokes and agents:
        agent = agents.pop()
        read = lambda path: open(f"ar/{company}/{path}", "r").read()
        instructions = read("All").replace("{agent}", agent) + read(agent)

        if agent in tools.bench:
            msgs = messages.from_string(tools.invoke(agent, run))
        else:
            msgs = list(filter(lambda msg: agent in (msg.sender, msg.recipient), history)) + run
            completion = llm.invoke(instructions, messages.to_string(msgs))
            sanity = lambda msg: msg.sender == agent and msg.recipient not in (msg.sender) and (msg.recipient != account or msg.sender == intake)
            msgs = messages.from_string(completion, sanity)

        run += msgs

        print(messages.to_string(msgs))
        print("--------------------------------------------")

        if len(msgs) == 1 and agent == intake:
            msg = msgs[0]
            if msg.recipient == account:
                messages.save(run)
                return msg.body
            else:
                agents.add(msg.recipient)
        elif msgs:
            for msg in msgs:
                if msg.recipient != account:
                    agents.add(msg.recipient)

    msg = Message(intake, account, "Could you repeat that?")
    run += [msg]
    messages.save(run)
    return msg.body

# invoke("account-375491", "Do you sell men's shoes?")
invoke("account-375491", "What's my balance?")
