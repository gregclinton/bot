const chat = {
    prompt: async prompt => {
        chat.waiting = true;

        function post(text) {
            const name = document.getElementById('chat').children.length % 2 ? 'ai' : 'me';
            const title = document.createElement('span');

            title.innerHTML = name
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

            post.scrollIntoView({ behavior: 'smooth' });
        }

        post(prompt);

        await fetch('/agent/prompts', {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: prompt
            })
        })
        .then(response => response.json())
        .then(o => {
            reply = o.content.replace(/\\/g, '\\\\');  // so markdown won't trample LaTex
            post(marked.parse(reply));
            chat.waiting = false;
        });
    },

    clear: () => {
        document.getElementById('chat').innerHTML = "";
        fetch('/agent/thread/current', { method: 'DELETE' });
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
            fetch('/agent/prompts/last', { method: 'DELETE' });
        }
    }
};

chat.clear();