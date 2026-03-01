import messages

for msg in messages.inbox("Balance"):
    messages.post("Balance", msg.frm, f"{msg.body}\nBalance is $13.55.")