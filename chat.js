const chat = {
    entity: "Plaza/Intake",
    thread: "375491",

    fetch: async prompt => {
        return fetch(`/mall/${chat.entity}/messages/${chat.thread}`, {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        })
    },

    post: data => {
        const name = document.getElementById('chat').children.length % 2 ? chat.entity : 'me';
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

        document.title = chat.entity;
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
            if (data.entity) {
                chat.entity = data.entity
                data.content = `You are now connected with ${data.entity}.`;
            } else {
                data.content = data.content.replace(/\\/g, '\\\\');  // so markdown won't trample LaTex
                data.content = marked.parse(data.content)
            }
            chat.post(data);
            chat.waiting = false;
    });
    },
};
