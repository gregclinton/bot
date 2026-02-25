import threads
import time
import llm

provider = "groq"
model = "openai/gpt-oss-20b"

while True:

    thread = threads.get("1000")
    if thread:
        print(llm.invoke(provider, model, "You are Hal.", open(thread).read()))

    thread = threads.get("1001")
    if thread:
        print(llm.invoke(provider, model, "You are Sally.", open(thread).read()))

    time.sleep(1)