document.title = 'hal';

const chat = {
    model: 'gpt-4.1-nano',

    models: {
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

    const models = document.getElementById('models');
    `
    gpt-4.1       openai
    gpt-4.1-mini  openai
    gpt-4.1-nano  openai
    o3            openai
    o4-mini       openai
    claude-3.7    anthropic  claude-3-7-sonnet-latest
    gemini-2.5    google     gemini-2.5-flash-preview-04-17
    grok-3        xai
    mistral-large mistral    mistral-large-latest
    llama-4       fireworks  llama4-maverick-instruct-basic
    qwen-3        fireworks  qwen3-235b-a22b
    deepseek-v3   nebius     deepseek-ai/DeepSeek-V3-0324
    prover        openrouter deepseek/deepseek-prover-v2:free
    `
    .trim().split('\n').forEach(row => {
        const [name, provider, model] = row.trim().split(/\s+/);
        const div = document.createElement('div');
        div.innerHTML = name;
        div.onclick = () => {
            const url = new URL(`/threads/${chat.thread}/model`, location.origin);

            url.search = new URLSearchParams({ provider, model: model || name });
            fetch(url, { method: 'PUT' });
            chat.model = name;
            chat.models.toggle();
        }
        models.appendChild(div);
    });
};

window.addEventListener('unload', () => {
    fetch(`/threads/${chat.thread}`, { method: 'DELETE' });
});