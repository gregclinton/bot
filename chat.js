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

            post.scrollIntoView({ behavior: 'smooth' });
        }

        post(prompt);

        await fetch('/company/messages', {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: prompt
            })
        })
        .then(response => response.json())
        .then(o => {
            post(o.content);
            chat.waiting = false;
        });
    },

    clear: () => {
        document.getElementById('chat').innerHTML = "";
        fetch('/company/messages', { method: 'DELETE' });
    }
};

chat.clear();