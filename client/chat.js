const chat = {
    fetch: async prompt => {
        return fetch(`/bot/threads/${chat.thread}/messages`, {
            method: 'POST',
            headers:  { 'Content-Type': 'text/plain' },
            body: prompt
        })
    },

    post: text => {
        const name = document.getElementById('chat').children.length % 2 ? "ai" : 'me';
        const title = document.createElement('span');

        title.innerHTML = name;
        title.classList.add('name');

        const top = document.createElement('div');

        top.append(title);

        const bottom = document.createElement('div');

        bottom.innerHTML = text;

        const post = document.createElement('div');
        post.append(top, bottom);
        post.classList.add('post');
        document.getElementById('chat').appendChild(post);

        Prism.highlightAll();
        MathJax.typesetPromise();

        document.title = "ai";
        post.scrollIntoView({ behavior: 'smooth' });
    },

    prompt: async (prompt, hide) => {
        chat.waiting = true;

        if (!hide) {
            chat.post(prompt);
        }

        await chat.fetch(prompt)
        .then(response => response.text())
        .then(text => {
            text = text.replace(/\\/g, '\\\\');  // so markdown won't trample LaTex
            text = marked.parse(text)
            chat.post(text);
            chat.waiting = false;
        });
    },

    clear: () => {
        document.getElementById('chat').innerHTML = "";
        fetch(`/bot/threads/${chat.thread}/messages`, { method: 'DELETE' });
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
            fetch(`/bot/threads/${chat.thread}/messages/last`, { method: 'DELETE' });
        }
    }
};

window.onload = () => {
    fetch('/bot/threads', { method: 'POST' })
    .then(response => response.text())
    .then(id => { chat.thread = id; });
};

window.addEventListener("unload", () => {
    fetch(`/bot/threads/${chat.thread}`, { method: 'DELETE' });
});