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

        if ('{['.includes(text[0])) {
            spec = JSON.parse(text);
            spec.layout ??= {}
            spec.layout.margin = { l: 50, r: 10, t: 50, b: 50 };
            Plotly.newPlot(bottom.id, spec);
        } else {
            bottom.innerHTML = text;
            Prism.highlightAll();
            MathJax.typesetPromise();
        }

        post.scrollIntoView({ behavior: 'smooth' });
    },

    prompt: async (prompt) => {
        chat.waiting = true;
        chat.post(prompt);

        await chat.fetch(prompt)
        .then(res => res.text())
        .then(text => {
            if (!'{['.includes(text[0])) {
                text = text.replace(/\\/g, '\\\\');  // so markdown won't trample LaTex
                text = marked.parse(text)
            }
            chat.post(text);
            chat.waiting = false;
        });
    },

    clear: () => {
        document.getElementById('chat').innerHTML = '';
        fetch(`/threads/${chat.thread}`, { method: 'DELETE' });
        fetch('/threads', { method: 'POST' }).then(res => res.text()).then(id => { chat.thread = id; });
    },

    paste: () => {
        navigator.clipboard.readText()
        .then(prompt => {
            if (prompt !== '') {
                chat.prompt(prompt);
            }
        })
    },

    redo: () => {
        const div = document.getElementById('chat');

        if (div.children.length > 1) {
            const prompt = div.lastChild.previousSibling.lastChild.innerHTML;

            chat.back();
            chat.prompt(prompt);
        }
    },

    back: () => {
        const div = document.getElementById('chat');

        if (div.children.length > 1) {
            div.removeChild(div.lastChild);
            div.removeChild(div.lastChild);
            fetch(`/threads/${chat.thread}/messages/last`, { method: 'DELETE' });
        }
    }
};

window.onload = async () => {
    fetch('/threads', { method: 'POST' }).then(res => res.text()).then(id => { chat.thread = id; });
};

window.addEventListener('unload', () => {
    fetch(`/threads/${chat.thread}`, { method: 'DELETE' });
});