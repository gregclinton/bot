import llm
import catalog
import messages
from messages import Message, load

company = "sephora"
intake = "Sales"

def process_tool(msg):
    if msg.recipient == "Catalog" and msg.sender == intake:
        return Message("Catalog", msg.sender, catalog.query(msg.body))
    return msg

def invoke(account, prompt):
    mgmt = f"{company}.txt"
    calls = f"{company}.calls.txt"
    msg = Message(account, intake, prompt)
    messages.append_to_file(calls, [msg])
    departments = set()
    departments.add(msg.recipient)

    max_llm_invokes = 10
    n_llm_invokes = 0

    while n_llm_invokes < max_llm_invokes and departments:
        department = departments.pop()

        msgs = load(mgmt, lambda msg: msg.sender in ("Management") and msg.recipient in (department, "company"))
        msgs += load(calls, lambda msg: msg.account == account and department in (msg.sender, msg.recipient))

        for i, msg in enumerate(msgs):
            msgs[i] = process_tool(msg)

        with open("instructions", "r") as file:
            instructions = file.read().replace("{department}", department)

        n_llm_invokes += 1
        completion = llm.invoke(instructions, messages.to_string(msgs))

        print(completion)
        print("--------------------------------------------")

        sanity = lambda msg: msg.sender == department and msg.recipient not in (msg.sender, "Management") and (msg.recipient != account or msg.sender == intake)
        msgs = messages.from_string(completion, sanity)

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

invoke("account-375491", "Do you sell men's shoes?")
# invoke("account-375491", "What's my balance?")
