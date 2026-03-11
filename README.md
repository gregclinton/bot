
I include a toy app under apps called wireless.
This is how I set it up.
```
mkdir ~/app
cd ~/app
sh ~/bot/apps/wireless/setup
```

Each worker's instructions can be found under its folder.
The toy wireless app has three workers. Here I'll show two:

Hal:
```
Preface your answer with one of the following:

To: Customer
To: Marketing
To: Sundries
To: Billing
To: Sales

Only use plain text, not markdown, in your anaswer.
You can use more than one To: throughout your response as neeeded.
Keep your answer short, professional and to the point.
Do not ask followup questions.
I'm paying by the token.

To Customer:
Go ahead. Ask your question.
```

Billing:
```
Forward balance questions with customer's account number to Balance calculator like so:

To: Balance
CX32145

To Hal:
Go ahead, Hal. Ask your question.
```

I export LLM API keys and then I run my workers.
```
cd ~/app
export GROQ_API_KEY=ASFJSADFLHHJFL
sh ~/bot/apps/wireless/run
```

In another terminal session, I poll for answers.

```
cd ~/app
while true; do python3 messages poll TLG15151515; sleep 0.2 done
```

I post questions, like so:

```
cd ~/app
python3 messages.py post TLG15151515 Hal "What is my balance?"
```

```
Customer:
To: Hal
Hello.

Hal:
To: Customer
Hello! I’m Hal, your help specialist. How can I assist you today?

Customer:
To: Hal
I’d like to know my balance.

Hal:
To: Customer
Sure, I’ll check that for you right away.

To: Billing
Please provide the current balance for this customer.

Billing:
To: Balance
balance?

Balance:
To: Billing
$12.37

Billing:
To: Hal
Your current balance is $12.37.

Hal:
To: Customer
Your current balance is $12.37. Let me know if there’s anything else I can help you with.
```

The source code for this bot is fewer than 200 lines of python.
This is where the world is heading.

I've been a programmer for over 30 years.
During that time I've used Pascal, C, C++, C#, rust,
javascript, typescript, html, css, xml, perl, python, R, julia
and even assembly language.

English (or some other natural language) is replacing python (or some other high level programming language)
just as C replaced assembly in the past.
Compilers came along then, just as now, LLM's are coming along.

Assembly language still exists, and some programmers still need to code with it.
Python and its brothers also still exist,
but more and more we'll need them less and speak to our computers in our native tongues more.

Hal, Billing and Sales in apps/wireless/workers use understandable English.
Programming computers from here on, will consist of just talking or writing to them.

You hear a lot about the high price of token generation.
I've designed this system to work well with inexpensive open source models.
I've been using gpt-oss-120b which at this time is 60 cents per million output tokens.
I've even seen OpenRouter offer that model for free.
See my llm.py for a list of other inference providers.

Also, since this system makes it easy to orchestrate many small specialized workers,
each worker uses a small context window, further reducing inference costs.

I run the bot on my own computer. I don't need to deploy it to the cloud.
Running it is extremely inexpensive and can even be free.
And it is under my control.

Workers receive instructions from me and messages from the customer and from other workers.
Each worker stores on disk all messages they've sent or received in per-user-account folders.
This way when a worker is called into action for a user,
it has a complete chronological transcript, a dossier as it were, for that user.
We have here a poor man's CRM.
When a user checks in a day or a month later, she won't have to repeat herself.

The idea of this bot is to power call centers.
I show a toy example.
Your toy example and real world examples are left as an excersise to the reader.