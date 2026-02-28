# python3 balance.py 

import messages

for msg in messages.inbox("Balance"):
    messages.post("Balance", msg.poster, f"{msg.body}\nBalance is $13.55.")