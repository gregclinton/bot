import threads
import time
import llm

# python3 threads.py post 1000 3000 "My name is Fred."

while True:
    invoke = lambda sys, user: llm.invoke("groq", "openai/gpt-oss-20b", sys, user)
    read = lambda *files: "\n\n".join(open(f"markdown/{f}.md").read() for f in files)

    owner = "1000"
    thread = threads.get(owner)
    if thread:
        threads.post(owner, owner, invoke(read("hal"), thread))

    owner = "1001"
    thread = threads.get(owner)
    if thread:
        threads.post(owner, owner, invoke(read("sally"), thread))

    time.sleep(1)