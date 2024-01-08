document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('container');
    const registerForm = document.querySelector('.sign-up form');
    const loginForm = document.querySelector('.sign-in form');
    const toggleLoginBtn = document.getElementById('login');
    const toggleRegisterBtn = document.getElementById('register');

    // Toggle between login and register forms
    toggleLoginBtn.addEventListener('click', function () {
        container.classList.remove("active");
    });

    toggleRegisterBtn.addEventListener('click', function () {
        container.classList.add("active");
    });
})

    // Register User
    registerForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(registerForm);
        const userData = {
            "username": formData.get('username').toString(),
            "email": formData.get('email').toString(),
            "password": formData.get('password').toString()
        };

        fetch('http://localhost:5000/users/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Registration failed');
            }
            return response.text(); 
        })
        .then(data => {
            console.log(data); 
            redirectToHome();
        })
        .catch(error => {
            console.error('Error:', error.message); // Handle error
        });
    });

    // Login User
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(loginForm);
        const userData = {
            "email": formData.get('email'),
            "password": formData.get('password')
        };

        fetch('/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('login failed');
            }
            return response.text(); 
        })
        .then(data => {
            const { access_token, user_id } = JSON.parse(data);
            localStorage.setItem('userId', user_id);
            console.log('Login successful' , user_id);
            redirectToHome();
        })
        .catch(error => {
            console.error('Error:', error.message); // Handle error
        });
    });


function redirectToHome() {
    window.location.href = "/welcome";
}
