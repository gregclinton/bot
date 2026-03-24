document.title = 'bot';

const chat = {
    account: 'TLG143623',
    worker: 'Hal',
    latest: 0,

    send: async () => {
        const e = document.getElementById('prompt')
        const prompt = e.value.trim()

        chat.show(chat.account, prompt, new Date() * 1000);
        e.value = '';
        fetch('/messages', {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({ from: chat.account, to: chat.worker, body: prompt })
        });
    },

    retrieve: async () => {
        fetch(`/messages/${chat.account}?timeout=30`)
        .then(res => res.json())
        .then(list => {
            list.forEach(item => {
                chat.show(item.from, item.body, item.timestamp);
                chat.latest = item.timestamp;

                if (item.from != chat.account)
                    chat.worker = item.from;
            });
            setTimeout(chat.retrieve, 100);
        })
    },

    show: (from, body, timestamp) => {
        const text = marked.parse(item.body);
        const title = document.createElement('span');
        const top = document.createElement('div');
        const bottom = document.createElement('div');
        const post = document.createElement('div');

        title.innerHTML = item.from === chat.account ? 'me' : item.from;
        title.classList.add('name');
        top.append(title);
        post.append(top, bottom);
        post.classList.add('post');
        document.getElementById('chat').appendChild(post);
        bottom.innerHTML = text;
        post.scrollIntoView({ behavior: 'smooth' });

        if (item.timestamp - chat.latest > 3600) {
            const d = new Date(item.timestamp * 1000);
            const now = new Date();
            const a = new Date(d).setHours(0, 0, 0, 0);
            const b = new Date(now).setHours(0, 0, 0, 0);
            const c = new Date(new Date(now).setDate(now.getDate() - 1)).setHours(0, 0, 0, 0);
            const date = a === b ? 'Today' : a === c ? 'Yesterday' : d.toLocaleDateString('en-US', {
                weekday: 'long',
                month: 'long',
                day: 'numeric'
            }) + (d.getFullYear() === now.getFullYear() ? '' : `, ${d.getFullYear()}`);
            const time = d.toLocaleTimeString('en-US', {
                hour: 'numeric',
                minute: '2-digit',
                hour12: true
            });
            const when = document.createElement('span');

            when.innerHTML = `${date} at ${time}`;
            when.classList.add('when');
            top.append(when);
        }
    }
};

window.onload = async () => {
    chat.retrieve();
};