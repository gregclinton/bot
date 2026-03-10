
I include a toy app under apps called wireless.
This is how you set it up.
```
mkdir ~/app
cd ~/app
sh ~/bot/apps/wireless/setup
```

The toy wireless app has three workers.
We write instructions for the workers.
Each worker's instructions can be found under the app.

For Hal:
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

For Billing:
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

Export your LLM API keys and Telegram BotFather token. Then run your workers.
```
cd ~/app
export GROQ_API_KEY=ASFJSADFLHHJFL
export TELEGRAM_TOKEN=ASFDAFDSFDFAFSAFSA
sh ~/bot/apps/wireless/run
```

In another terminal session, poll Telegram:

```
cd ~/app
export TELEGRAM_TOKEN=ASFDAFDSFDFAFSAFSA
while true; do python3 telegram.py updates; done
```

Then, you or a friend go to Telegram and chat with your Bot.

You will see messages like these:

```
Customer:
To: Hal
hello

Hal:
To: Customer
Hello! I’m Hal, your help specialist. How can I assist you today?

Customer:
To: Hal
I’d like to know my balance

Hal:
To: Customer
Sure, I’ll check that for you right away.

To: Billing
Please provide the current balance for this customer.

Billing:
To: Balance
balance?

Balance:
$12.37

Billing:
To: Hal
Your current balance is $12.37.

Hal:
To: Customer
Your current balance is $12.37. Let me know if there’s anything else I can help you with.
```

The source code for this bot (in the bot subfolder) is fewer than 200 lines of python.
This is where the world is heading.

I've been a programmer for over 30 years.
During that time I've used Pascal, C, C++, C#, rust,
javascript, typescript, html, css, xml, perl, python, R, julia
and even assembly language.

English (or some other natural language) is replacing python (or someo other high level programming language)
just as C replaced assembly in the past.
Compilers came along then, just as now, LLM's came along.

Now assembly language still exists, and some programmers still need to code with it.
Python and its brothers still exist, 
but more and more we'll need them less and speak to our computers in our native tongues.

If you look at the apps/wireless/workers Hal, Billing and Sales, you'll find understandable English.
Programming computers from here on, will consist of just talking or writing to them.





















