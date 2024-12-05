const chat = {
    fetch: async prompt => {
        return fetch(`/mall/threads/${chat.thread}/messages`, {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        })
    },

    post: data => {
        const name = document.getElementById('chat').children.length % 2 ? "ai" : 'me';
        const title = document.createElement('span');

        title.innerHTML = name;
        title.classList.add('name');

        const top = document.createElement('div');

        top.append(title);

        const bottom = document.createElement('div');

        bottom.innerHTML = data.content;

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
            chat.post({content: prompt});
        }

        await chat.fetch(prompt)
        .then(response => response.json())
        .then(data => {
            data.content = data.content.replace(/\\/g, '\\\\');  // so markdown won't trample LaTex
            data.content = marked.parse(data.content)
            chat.post(data);
            chat.waiting = false;
        });
    },

    clear: () => {
        document.getElementById('chat').innerHTML = "";
        fetch(`/mall/threads/${chat.thread}/messages`, { method: 'DELETE' });
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
            fetch(`/mall/threads/${chat.thread}/messages/last`, { method: 'DELETE' });
        }
    }
};

window.onload = () => {
    fetch('/mall/threads', {
        method: 'POST',
        headers:  { 'Content-Type': 'application/json' },
        body: '{}'
    })
    .then(response => response.json())
    .then(data => {
        chat.thread = data['id'];
    });
};

window.addEventListener("unload", () => {
    chat.clear();
});