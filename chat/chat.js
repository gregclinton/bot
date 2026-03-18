document.title = 'bot';

const chat = {
    me: 'TLG143623',
    worker: 'Hal',
    timestamp: 0,

    send: async () => {
        const e = document.getElementById('prompt')
        const prompt = e.value.trim()

        chat.show('me', prompt);
        e.value = '';
        fetch('/messages', {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({ from: chat.me, to: chat.worker, body: prompt })
        });
    },

    retrieve: async () => {
        fetch(`/messages/${chat.me}?timestamp=${chat.timestamp}&timeout=30`)
        .then(res => res.json())
        .then(list => {
            list.forEach(item => {
                chat.worker = item.from;
                chat.timestamp = item.timestamp;
                chat.show(item.from, marked.parse(item.body));
            });
            setTimeout(chat.retrieve, 100);
        })
    },

    show: (name, text) => {
        const title = document.createElement('span');
        const top = document.createElement('div');
        const bottom = document.createElement('div');
        const post = document.createElement('div');

        title.innerHTML = name;
        title.classList.add('name');
        top.append(title);
        post.append(top, bottom);
        post.classList.add('post');
        document.getElementById('chat').appendChild(post);
        bottom.innerHTML = text;
        post.scrollIntoView({ behavior: 'smooth' });
    },
};

window.onload = async () => {
    chat.retrieve();
};