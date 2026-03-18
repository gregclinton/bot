document.title = 'bot';

const chat = {
    account: 'TLG143623',
    worker: 'Hal',
    after: 0,

    send: async () => {
        const e = document.getElementById('prompt')
        const prompt = e.value.trim()

        e.value = '';
        fetch('/messages', {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({ from: chat.account, to: chat.worker, body: prompt })
        });
    },

    retrieve: async () => {
        fetch(`/messages/${chat.worker}/${chat.account}?after=${chat.after}&timeout=30`)
        .then(res => res.json())
        .then(list => {
            list.forEach(item => {
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

                chat.worker = item.from;
                chat.after = item.order;
            });
            setTimeout(chat.retrieve, 100);
        })
    },
};

window.onload = async () => {
    chat.retrieve();
};