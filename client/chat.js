document.title = 'hal';

const chat = {
    model: 'gpt-4o-mini',

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
        document.getElementById('chat').innerHTML = '';
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
    `
    o3-mini       openai
    gpt-4.5       openai    gpt-4.5-preview
    gpt-4o        openai
    gpt-4o-mini   openai
    claude-3.7    anthropic claude-3-7-sonnet-latest
    gemini-2.5    google    gemini-2.5-pro-exp-03-25
    grok-2        xai
    mistral-large mistral   mistral-large-latest
    llama-3.3     together  meta-llama/Llama-3.3-70B-Instruct-Turbo
    deepseek-v3   nebius    deepseek-ai/DeepSeek-V3-0324
    deepseek-r1   together  deepseek-ai/DeepSeek-R1
    qwen-2.5      groq      qwen-2.5-32b
    `
    .trim().split('\n').forEach(row => {
        const [name, provider, model] = row.trim().split(/\s+/);
        const div = document.createElement('div');
        const url = `/threads/${chat.thread}/model?provider=${provider}&model=${model || name}`;

        div.innerHTML = name;
        div.onclick = () => {
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