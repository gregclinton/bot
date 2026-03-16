document.title = 'bot';

const chat = {
    from: 'TLG143623',
    to: "Hal",

    send: async () => {
        const e = document.getElementById("prompt")
        const prompt = e.value.trim()

        chat.show("me", prompt);
        e.value = '';
        fetch(`/messages`, {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({ from: chat.from, to: chat.to, body: prompt })
        });
    },

    retrieve: async () => {
        fetch(`/messages/${chat.from}?timeout=30`)
        .then(res => res.json())
        .then(list => {
            list.forEach(item => {
                chat.to = item.from;
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

    clear: () => {
        document.getElementById('chat').innerHTML = '';
    }
};

window.onload = async () => {
    chat.retrieve();
};