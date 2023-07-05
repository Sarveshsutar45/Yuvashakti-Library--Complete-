s
const form = document.getElementById('login-form');

form.addEventListener('submit', e => {
    e.preventDefault();

    const username = form.username.value;
    const password = form.password.value;

    fetch('/admin/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: username, password: password})
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/dashboard';
        } else {
            alert('Invalid username or password. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

});

