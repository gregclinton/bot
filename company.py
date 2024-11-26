import llm
import messages
from messages import Message, load
import os

def invoke(account, prompt):
    company = "sephora"
    mgmt = f"{company}.txt"
    calls = f"{company}.calls.txt"
    msg = Message(account, "Sales", prompt)
    messages.append_to_file(calls, [msg])
    departments = set()
    departments.add(msg.recipient)

    max_llm_invokes = 10
    n_llm_invokes = 0

    while n_llm_invokes < max_llm_invokes and departments:
        department = departments.pop()

        msgs = load(mgmt, lambda msg: msg.sender in ("Management") and msg.recipient in (department, "company"))
        msgs += load(calls, lambda msg: msg.account == account and department in (msg.sender, msg.recipient))

        with open("instructions", "r") as file:
            instructions = file.read().replace("{department}", department)

        n_llm_invokes += 1
        completion = llm.invoke(instructions, messages.to_string(msgs))

        print(completion)
        print("--------------------------------------------")

        sanity = lambda msg: msg.sender == department and msg.recipient not in (msg.sender, "Management") and (msg.recipient != account or msg.sender == "Sales")
        msgs = messages.from_string(completion, sanity)

        if len(msgs) == 1 and department == "Sales":
            messages.append_to_file(calls, msgs)
            if msgs[0].recipient == account:
                return msgs[0].body
            else:
                departments.add(msg.recipient)
        elif msgs:
            for msg in msgs:
                if msg.recipient != account:
                    messages.append_to_file(calls, [msg])
                    departments.add(msg.recipient)

    msg = Message("Sales", account, "Could you repeat that?")
    messages.append_to_file(calls, [msg])
    return msg.body

invoke("account-375491", "I want to know my balance.")
