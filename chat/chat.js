document.title = 'hal';

const chat = {
    account: 'TLG143623',

    correspondent: "Hal",

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
            body: JSON.stringify({ from: chat.account, to: chat.correspondent, body: prompt })
        });
    },

    clear: () => {
        document.getElementById('chat').innerHTML = '';
    },

    run: () => {
        fetch(`/messages/${chat.account}?timeout=30`)
        .then(res => res.json())
        .then(list => {
            chat.correspondent = msg.frm;
            list.forEach(msg => chat.post(msg.frm, marked.parse(msg.body)));
            setTimeout(chat.run, 500);
        });
    }
};

window.onload = async () => {
    chat.run();
};
