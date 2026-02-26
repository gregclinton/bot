import messages
import time
import llm

while True:
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)

    me = "Hal"
    for msg in messages.mine(me):
        print(msg.read_text())
        print(invoke("", msg.read_text()))
    time.sleep(1)