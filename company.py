import llm
import messages
from messages import Message, load
import tools

def invoke(account, prompt):
    company = "sephora"
    intake = "Intake"
    calls = "messages.txt"
    departments = set()
    max_llm_invokes = 10
    llm.reset_counter()

    msg = Message(account, intake, prompt)
    messages.append_to_file(calls, [msg])
    departments.add(msg.recipient)

    while llm.counter < max_llm_invokes and departments:
        department = departments.pop()

        read = lambda path: open(f"ar/{company}/{path}", "r").read()
        instructions = read("All").replace("{department}", department) + read(department)

        msgs = load(calls, lambda msg: msg.account == account and department in (msg.sender, msg.recipient))

        completion = tools.invoke(department, load(calls)) if department in tools.bench else llm.invoke(instructions, messages.to_string(msgs))
        sanity = lambda msg: msg.sender == department and msg.recipient not in (msg.sender) and (msg.recipient != account or msg.sender == intake)
        msgs = messages.from_string(completion, sanity)

        print(messages.to_string(msgs))
        print("--------------------------------------------")

        if len(msgs) == 1 and department == intake:
            msg = msgs[0]
            messages.append_to_file(calls, [msg])
            if msg.recipient == account:
                return msg.body
            else:
                departments.add(msg.recipient)
        elif msgs:
            for msg in msgs:
                if msg.recipient != account:
                    messages.append_to_file(calls, [msg])
                    departments.add(msg.recipient)

    msg = Message(intake, account, "Could you repeat that?")
    messages.append_to_file(calls, [msg])
    return msg.body

# invoke("account-375491", "Do you sell men's shoes?")
invoke("account-375491", "What's my balance?")
