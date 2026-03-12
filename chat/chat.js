document.title = 'hal';

const chat = {
    from: 'TLG143623',
    to: "Hal",

    post: (name, text) => {
        const title = document.createElement('span');

        title.innerHTML = name;
        title.classList.add('name');

        const top = document.createElement('div');

        top.append(title);

        const bottom = document.createElement('div');

        const post = document.createElement('div');
        post.append(top, bottom);
        post.classList.add('post');
        document.getElementById('chat').appendChild(post);

        bottom.innerHTML = text;

        post.scrollIntoView({ behavior: 'smooth' });
    },

    prompt: async () => {
        const e = document.getElementById("prompt")
        const prompt = e.value.trim()
        chat.post("me", prompt);
        e.value = '';
        fetch(`/messages`, {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({ from: chat.from, to: chat.to, body: prompt })
        });

        chat.retrieve();
    },

    clear: () => {
        document.getElementById('chat').innerHTML = '';
    },

    retrieve: () => {
        fetch(`/messages/${chat.from}?timeout=30`)
        .then(res => res.json())
        .then(list => {
            list.forEach(item => {
                chat.to = item.from;
                chat.post(item.from, marked.parse(item.body));
            });
            setTimeout(chat.retrieve, 100);
        })
    }
};

window.onload = async () => {
    chat.retrieve();
};

