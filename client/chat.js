document.title = 'hal';

const chat = {
    post: (name, text) => {
        const title = document.createElement('span');

        title.innerHTML = name;
        title.classList.add('name');

        const top = document.createElement('div');

        top.append(title);

        const bottom = document.createElement('div');

        const post = document.createElement('div');
        post.append(top, bottom);
        post.classList.add('post');
        document.getElementById('chat').appendChild(post);

        bottom.innerHTML = text;

        post.scrollIntoView({ behavior: 'smooth' });
    },

    prompt: async () => {
        const e = document.getElementById("prompt")
        const prompt = e.value.trim()
        chat.post("me", prompt);
        e.value = '';
        fetch(`/messages`, {
            method: 'POST',
            headers:  { 'Content-Type': 'text/plain' },
            body: prompt
        })
    },

    clear: () => {
        document.getElementById('chat').innerHTML = '';
    },

    run: () => {
      fetch('/messages')
        .then(res => res.json())
        .then(list => {
            list.forEach(text => chat.post("hal", marked.parse(text))));
            setTimeout(chat.run, 1000)
        }
    }
};

window.onload = async () => {
    chat.run();
};
