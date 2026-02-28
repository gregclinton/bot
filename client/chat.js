document.title = 'hal';

const chat = {
    fetch: async prompt => {
        return fetch(`/threads/${chat.thread}/messages`, {
            method: 'POST',
            headers:  { 'Content-Type': 'text/plain' },
            body: prompt
        })
    },

    post: text => {
        const count = document.getElementById('chat').children.length;
        const name =  count % 2 ? document.title : 'me';
        const title = document.createElement('span');

        title.innerHTML = name;
        title.classList.add('name');

        const top = document.createElement('div');

        top.append(title);

        const bottom = document.createElement('div');

        bottom.id = 'id-' + (1000 + count);

        const post = document.createElement('div');
        post.append(top, bottom);
        post.classList.add('post');
        document.getElementById('chat').appendChild(post);

        bottom.innerHTML = text;
        Prism.highlightAll();

        post.scrollIntoView({ behavior: 'smooth' });
    },

    prompt: async () => {
        chat.waiting = true;
        const e = document.getElementById("prompt")
        const prompt = e.value.trim()
        chat.post(prompt);
        e.value = '';

        await chat.fetch(prompt)
        .then(res => res.text())
        .then(text => {
            chat.post(marked.parse(text));
            chat.waiting = false;
        });
    },

    clear: () => {
        document.getElementById('chat').innerHTML = '';
        fetch(`/threads/${chat.thread}`, { method: 'DELETE' });
        fetch('/threads', { method: 'POST' }).then(res => res.text()).then(id => { chat.thread = id; });
    }
};

window.onload = async () => {
    fetch('/threads', { method: 'POST' }).then(res => res.text()).then(id => { chat.thread = id; });
};

window.addEventListener('unload', () => {
    fetch(`/threads/${chat.thread}`, { method: 'DELETE' });
});