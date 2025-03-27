document.title = "hal";

const chat = {
    model: "gpt-4o-mini",

    models: {
        list: ("o3-mini gpt-4.5 gpt-4o gpt-4o-mini mistral-large " +
            "gemini-2.5 claude-3-7 llama-3.3 deepseek-v3 deepseek-r1").split(" "),

        toggle: () => {
            const models = document.getElementById('models');
            models.hidden = !models.hidden;

            document.getElementById('chat').hidden = !models.hidden;
        }
    },

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

        if (name !== 'me') {
            const model = document.createElement('span');

            model.classList.add('model');
            model.innerHTML = chat.model;
            top.append(model);
        }

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

    prompt: async (prompt, hide) => {
        chat.waiting = true;

        if (!hide) {
            chat.post(prompt);
        }

        await chat.fetch(prompt)
        .then(response => response.text())
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
        document.getElementById('chat').innerHTML = "";
        fetch(`/threads/${chat.thread}/messages`, { method: 'DELETE' });
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

window.onload = () => {
    fetch('/threads', { method: 'POST' })
    .then(response => response.text())
    .then(id => { chat.thread = id; });

    const models = document.getElementById('models');

    chat.models.list.forEach(model => {
        const item = document.createElement('div');

        item.innerHTML = model + ' ';
        item.onclick = () => {
            chat.model = model;

            fetch(`/threads/${chat.thread}/model?model=${model}`, { method: 'PUT' });
            chat.models.toggle();
        }
        models.appendChild(item);
    });
};

window.addEventListener("unload", () => {
    fetch(`/threads/${chat.thread}`, { method: 'DELETE' });
});