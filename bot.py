import threads
import time
import llm

while True:
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)

    thread = threads.get("1000")
    if thread:
        print(invoke("You are Hal.",  thread))

    thread = threads.get("1001")
    if thread:
        print(invoke("You are Sally.",  thread))

    time.sleep(1)