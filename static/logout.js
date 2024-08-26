async function logout(event) {
    event.preventDefault();
    const response = await fetch('/logout', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        window.location.href = '/login';
    } else {
        alert('Logout failed');
    }
}
