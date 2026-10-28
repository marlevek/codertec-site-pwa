// Adds a server-signed token to the contact forms; contact.php rejects posts without it.
(function () {
    const forms = document.querySelectorAll('form[action="/contact.php"]');
    if (!forms.length) return;

    function fetchToken() {
        return fetch('/contact-token.php', { cache: 'no-store', credentials: 'same-origin' })
            .then(res => res.ok ? res.json() : {})
            .then(data => data.token || '')
            .catch(() => '');
    }

    forms.forEach(form => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'form_token';
        form.appendChild(input);
        fetchToken().then(token => { if (!input.value) input.value = token; });

        form.addEventListener('submit', event => {
            if (input.value) return;
            event.preventDefault();
            fetchToken().then(token => {
                input.value = token;
                // The server requires a few seconds between issuing and submitting.
                setTimeout(() => form.submit(), 3500);
            });
        });
    });
})();
