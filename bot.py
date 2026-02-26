import threads
import time
import llm

# python3 threads.py post 1000 3000 "My name is Fred."

while True:
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)
    read = lambda *files: "\n\n".join(open(f"markdown/{f}.md").read() for f in files)

    thread = threads.get("1000")
    if thread:
        print(invoke(read("hal"), thread))

    thread = threads.get("1001")
    if thread:
        print(invoke(read("sally"), thread))

    time.sleep(1)