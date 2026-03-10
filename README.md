
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
You are Hal, our help specialist.
Below is communication from Customer.
Do your best to understand and respond.

You can ask for help from other departments if needed.

Always preface your response with one of the following:

To: Customer
To: Marketing
To: Sundries
To: Billing
To: Sales

Do not use markdown in your response.

Never mention account numbers.
Our system automatically includes that detail to departments as needed.

You can use more than one To: throughout your response as neeeded.

To Customer:
Go ahead. Introduce yourself to Hal. He is our help specialist.
```

Billing:
```
You work in Billing.

Below is communication from Hal, our help specialist.

Forward balance questions to Balance like so:
To: Balance
balance?

Always preface your response with one of the following:

To: Hal
To: Balance

Do not use markdown in your response.

Never mention account numbers.
Our system automatically includes that detail to departments as needed.

To Hal:
Go ahead, Hal. Billing will handle your request.
```

I export LLM API keys and Telegram BotFather token. Then I run my workers.
```
cd ~/app
export GROQ_API_KEY=ASFJSADFLHHJFL
export TELEGRAM_TOKEN=ASFDAFDSFDFAFSAFSA
sh ~/bot/apps/wireless/run
```

In another terminal session, I poll Telegram:

```
cd ~/app
export TELEGRAM_TOKEN=ASFDAFDSFDFAFSAFSA
while true; do python3 telegram.py updates; done
```

I go to Telegram and chat with my bot and see these messages logged:

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

I am new to the Telegram product, but I was extremely blown away by how easy it was to use
and how practical and useful I think it will become in this new LLM world.
My telegram.py code is all of 35 lines.

Consider the secret sauce (well not so secret, open source, actually) of this program, mainly in worker.py.
Workers receive instructions from me and then receive messages from Telegram and from other workers.
Each worker stores on disk all messages they've sent or received in per-user-account folders.
This way when a worker is called into action for a user,
it has a complete chronological transcript, a dossier as it were, for that user.
We have here a poor man's CRM.
When a user checks in a day or a month later, she won't have to repeat herself.

The idea of this bot is to power call centers.
I show a toy example.
Your toy example and real world examples are left as an excersise to the reader.




























