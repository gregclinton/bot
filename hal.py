import threads
import time
import llm

while True:
    thread = threads.get("/tmp/threads/1000")
    if thread:
        print(llm.invoke("groq", "openai/gpt-oss-20b", "You are Hal.", open(thread).read()))
    time.sleep(1)