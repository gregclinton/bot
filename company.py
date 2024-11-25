# sudo docker run -v `pwd`:/root -w /root company:latest python3 company.py

import llm
from messages import Messages

company = "sephora"
path = company + ".txt"
departments = Messages.recipients(path, lambda msg: msg.recipient != "company")

for department in ["Sales"]:
    account = None

    for msg in Messages.load("xxx.txt", lambda msg: msg.recipient == department):
        account = msg.account

    if not account:
        continue

    msgs = Messages.load(path, lambda msg: msg.sender in ("Management") and msg.recipient in (department, "company"))
    msgs += Messages.load("xxx.txt", lambda msg: msg.account == account and department in (msg.sender, msg.recipient))

    instruction = f"You are a worker in {department}. "
    instruction += "Take care of messages to you only if they require a reply. "
    instruction += "The messages are shown in chronological order. "

    completion = llm.invoke(instruction, Messages.to_string(Messages.load("mail.txt") + msgs))

    print(Messages.to_string(msgs + Messages.from_string(completion)))
