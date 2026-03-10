
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
Your name is Hal.
Below you will see a customer request.
Do your best to understand and answer it.

You can ask for help from our other departments.

To send a message, just specify the To: on one line and then the message.

See below how to send out multiple messages:

To: Sundries
Have you looked at the customer's inquiries yet?
-------------------
To: Marketing
Is the customer due for an appointment?

Do not use markdown.

We have these departments:
    Marketing
    Sundries
    Billing
    Sales
```

For Billing:
```
You work in Billing.
Below you will see a message from Hal.
Hal works the phone desk answering customer questions.
Reply to Hal's question like in the sample below.

To: Hal
Customer TLG12345678 is current.

If Hal asks for a customer's balance,
you can use our Balance tool
as formatted in sample below.

To: Balance
ID:TLG12345678

You will later receive a message with the result.
```

For Sales:
```
You work in Sales at a wireless phone company.

Below you will see a message from Hal.
Hal works the phone desk answering customer questions.
Do your best to understand the question and answer it.

You can reply to Hal's request as in the sample below.

To: Hal
Yes, stores will be open on Labor Day.

Currently we are not holding any promotions.

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
From: TLG5151551515
To: Hal
Account: TLG5151551515
what is my balance?
==========================
From: Hal
To: Billing
Account: TLG5151551515
Could you provide the current balance for account TLG5151551515?
==========================
From: Billing
To: Balance
Account: TLG5151551515
ID:TLG5151551515
==========================
From: Balance
To: Billing
Account: TLG5151551515
Customer TLG5151551515 has a balance of $12.37.
==========================
From: Billing
To: Hal
Account: TLG5151551515
Customer TLG5151551515 has a balance of $12.37.
==========================
From: Hal
To: TLG5151551515
Account: TLG5151551515
Your current balance is $12.37.
==========================
```