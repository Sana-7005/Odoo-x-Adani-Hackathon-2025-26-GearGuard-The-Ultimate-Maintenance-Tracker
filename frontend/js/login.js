// Login Page JavaScript

const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const errorMessage = document.getElementById('errorMessage');

// Validation functions
function validateEmail(email) {
    // Check if email ends with @gmail.com
    const gmailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
    return gmailRegex.test(email);
}

function validatePassword(password) {
    // Check if password is at least 8 characters
    return password.length >= 8;
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Real-time validation
emailInput.addEventListener('blur', function() {
    const emailError = document.getElementById('emailError');
    if (this.value && !validateEmail(this.value)) {
        emailError.textContent = 'Please enter a valid Gmail address';
        this.classList.add('error');
    } else {
        emailError.textContent = '';
        this.classList.remove('error');
    }
});

passwordInput.addEventListener('blur', function() {
    const passwordError = document.getElementById('passwordError');
    if (this.value && !validatePassword(this.value)) {
        passwordError.textContent = 'Password must be at least 8 characters';
        this.classList.add('error');
    } else {
        passwordError.textContent = '';
        this.classList.remove('error');
    }
});

// Form submission
loginForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    hideError();
    
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    
    // Validate email
    if (!validateEmail(email)) {
        showError('Please enter a valid Gmail address (@gmail.com)');
        emailInput.focus();
        return;
    }
    
    // Validate password
    if (!validatePassword(password)) {
        showError('Password must be at least 8 characters');
        passwordInput.focus();
        return;
    }
    
    // Show loading state
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.querySelector('.btn-loader');
    const submitBtn = loginForm.querySelector('button[type="submit"]');
    
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    submitBtn.disabled = true;
    
    try {
        // Send login request to backend
        const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Store session token
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('userEmail', email);
            localStorage.setItem('userName', data.user.full_name || email);
            
            // Redirect to dashboard
            window.location.href = 'index.html';
        } else {
            showError(data.error || 'Invalid email or password');
            btnText.style.display = 'inline-block';
            btnLoader.style.display = 'none';
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('Unable to connect to server. Please try again.');
        btnText.style.display = 'inline-block';
        btnLoader.style.display = 'none';
        submitBtn.disabled = false;
    }
});

// Check if already logged in
window.addEventListener('DOMContentLoaded', function() {
    const authToken = localStorage.getItem('authToken');
    if (authToken) {
        // Verify token is still valid
        fetch('http://localhost:5000/api/auth/verify', {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = 'index.html';
            } else {
                localStorage.removeItem('authToken');
            }
        })
        .catch(() => {
            localStorage.removeItem('authToken');
        });
    }
});
