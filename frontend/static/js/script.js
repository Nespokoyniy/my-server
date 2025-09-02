document.addEventListener('DOMContentLoaded', () => {
    const registerButton = document.getElementById('registerBtn');
    const loginButton = document.getElementById('loginBtn');

    if (registerButton) {
        registerButton.addEventListener('click', () => {
            window.location.href = '/register';
        });
    }

    if (loginButton) {
        loginButton.addEventListener('click', () => {
            window.location.href = '/login';
        });
    }
});

