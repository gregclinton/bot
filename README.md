
I include a toy app under apps called wireless.
This is how you set it up.
```
mkdir ~/app
cd ~/app
sh ~/bot/apps/wireless/setup
```

The toy wireless app has three workers.
We write instructions for the workers.
The instructions are in the workers folder under the app.

For Hal:
```
Your name is Hal.
You will be receiving messages from customers.
You will post answers to them.

If needed you can ask for help from other departments.

See below how to send out multiple posts:

From: Hal
To: Sundries
Have you looked at customer TLG12345678's inquiries yet?
-------------------
From: Hal
To: Marketing
Is customer TLG12345678 due for an appointment?

Do not supply a Subject: line and do not use markdown.

Currently we only have the following two departments: Billing, Sales
```

For Billing:
```
You work in Billing.
You will be receiving messages from Hal.
Hal works the phone desk answering customer questions.
Reply to Hal's questions like in the sample below.

From: Billing
To: Hal
Customer TLG12345678 is in arrears.

If Hal asks for a customer's balance,
you can use our Balance tool
as formatted in sample below.

From: Billing
To: Balance
Account:TLG12345678

You will later receive a message with the result.
```

For Sales:
```
You work in Sales at a wireless phone company.

Currently we are not holding any promotions.
I will notify you if this changes.

You will be receiving messages from Hal.
Hal works the phone desk answering customer questions.
You wil reply to Hal's inquiries as in the sample below.

From: Sales
To: Hal
Yes, stores will be open on Labor Day.
```

Export your LLM API keys and Telegram BotFather token. Then run your workers.
```
cd ~/app
export GROQ_API_KEY=ASFJSADFLHHJFLAJDFSAFHASLKHAFLHJ
export TELEGRAM_TOKEN=ASFDAFDSF:DFAFSAFSAFAFAFASDFAFAFAADFAFASF
sh ~/bot/apps/wireless/run
```

In another terminal session, poll Telegram:

```
cd ~/app
export TELEGRAM_TOKEN=ASFDAFDSF:DFAFSAFSAFAFAFASDFAFAFAADFAFASF
while true; do python3 telegram.py updates; done
```

Then, you or a friend go to Telegram and chat with your Bot.

You will see messages like these:

```
From: TLG8616785797
To: Hal
What is my balance?
==========================
From: Hal
To: Billing
What is the balance for customer TLG8616785797?
==========================
From: Billing
To: Balance
Account:TLG8616785797
==========================
From: Balance
To: Billing
The balance for TLG8616785797 is $12.37.
==========================
From: Billing
To: Balance
Account:TLG8616785797
==========================
From: Balance
To: Billing
The balance for TLG8616785797 is $12.37.
==========================
From: Billing
To: Hal
Customer TLG8616785797 balance is $12.37.
==========================
From: Hal
To: 8616785797
Your current balance is $12.37.
==========================
```