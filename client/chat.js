document.title = 'hal';

const chat = {
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
            body: JSON.stringify({ frm: "CX143623", to: "Hal", body: prompt })
        });
    },

    clear: () => {
        document.getElementById('chat').innerHTML = '';
    },

    run: () => {
        fetch('/messages/CX143623')
        .then(res => res.json())
        .then(list => {
            list.forEach(msg => chat.post(msg.frm, marked.parse(msg.body)));
            setTimeout(chat.run, 1000);
        });
    }
};

window.onload = async () => {
    chat.run();
};
