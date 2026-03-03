### The big picture

This is a CRM.

The idea is to make it easy and cheap for small mom-and-pop operations to set up, maintain and deploy LLM assistance for their customers.
Years ago, small businesses figured out who to call to get web sites set up for them. It wasn't that hard.
Getting LLM capability hasn't been easy. Up till now. That is what I'm trying to solve.

This project is in a very early stage. I'm the only one that uses it. And I don't know yet how logins will work.

But ignoring the security details for now, I want to give the big picture.

A business can set up an app for itself. This is very easy to do and we'll get into the details further below.

Once the app is set up, a customer of the business can log into the web site and type/talk with a chat assistant.
The chat assistant will be front and center for the web site. Maybe even the entirety of it.

The customer goes to the app and asks about a recent purchase or an upcoming appointment or directions or suggestions, etc., etc.
The chat assistant is available 24/7, responds instantly, remembers all past interactions, doesn't make customers repeat themselves and there are no hold times,
And the assistant is smart.

I'll check this README in for now. I'm just getting started. Stay posted.

### Why it's cheap
Need to discuss
- runpod prices
- model prices
- specialized small workers

### The way it was (and still is)
Need to discuss
- my bad experiences with my wireless carrier, the dmv, the irs, insurance, doctors, etc.

### The way it should be
Need to discuss
- 24 / 7
- no days off
- no holds
- no need to repeat myself
- no phone trees
- no bad moods, no bad connections, difficult accents
- everything is saved

### Where can this be used

I started out mentioning mom-and-pop businesses.

### Running on runpod
Need to discuss
- Dockerfile and docker hub
- Template
- Storage
- GPU vs CPU
- secrets
- pod id

### Introducing workers

```text
Your name is Hal.
You will be receiving messages from customers.
You will post answers to them.

A post looks like this:

From: Hal
To: CX123456
Your balance is $12.34.

Be sure to put the From: on the first line, the To: on the second line and the body of the post on the following lines.

You might not know the answer to a question.
You can post questions to Billing or just say you don't know.

Here is an example:

From: Hal
To: Billing
Please tell me the balance for customer CX123456.

If you need to send out more than one message, separate them by a line of hyphens like so: -------------------
```

```text
You work in Billing.
You will be receiving messages from Hal.
Hal works the phone desk answering customer questions.
You will reply by posting to Hal.
Put From: Billing on the first line of your response, To: Hal on the second line and put the body of your post on the following lines.

If Hal asks for a customer's balance, you can use our Balance tool as shown in the example below.
You will later receive a message with the result.

From: Billing
To: Balance
Account: CX345678
```

### Introducing tools

```python
import messages

tool = "Balance"

for msg in messages.inbox(tool):
    account = msg.body.split(":")[1].strip()

    # for this toy example we fake it
    # but here you would access your company's systems
    # to get the real balance
    balance = 13.55

    messages.post(tool, msg.frm, f"Account balance for {account} is ${balance}.")
```

### Introducing models
Need to discuss
- models (open vs frontier)
- inference providers
- API and API keys
- different models for diferent workers

### Introducing messages and threads
Need to discuss
- From, To, Body
- message threads based on customer accounts
- imagine all the advantages a business would have analyzing threads

### Introducing apps

### The context window

### Go remote

### The chat box

```text
From: CX143623
To: Hal
Hello. My name is Fred. What is my balance?
```

Need to discuss
- typing vs talking
- clear the screen
- it can be like a feed

### Say "no" to code (and "yes" to English or Spanish or whatever)
Need to discuss
- the Claude code and Codex mania
- C vs assembly, Python vs C, English vs Python