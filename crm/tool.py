import sys
import messages

tool = sys.argv[1:]

for msg in messages.inbox(tool):
    account = msg.body.split(":")[1].strip()

    # for this toy example we fake it
    # but here you would access your company's systems
    # to get the real balance
    if tool == "Balance":
        balance = 13.55
        result = f"Account balance for {account} is ${balance}."

    messages.post(tool, msg.frm, result)