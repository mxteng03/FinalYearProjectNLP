async function login(event) {
    event.preventDefault();
    const formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        remember: document.querySelector('input[type="checkbox"]').checked
    };

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        console.log(result);
        alert(result.message);

        if (response.ok) {
            window.location.href = result.redirect;
            document.getElementById('loginForm').reset();
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login. Please try again.');
    }
}
