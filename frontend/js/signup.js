// Signup Page JavaScript

const signupForm = document.getElementById('signupForm');
const fullNameInput = document.getElementById('fullName');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');

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

function validateName(name) {
    return name.trim().length >= 2;
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    successMessage.style.display = 'none';
}

function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.style.display = 'block';
    errorMessage.style.display = 'none';
}

function hideMessages() {
    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';
}

// Real-time validation
fullNameInput.addEventListener('blur', function() {
    const nameError = document.getElementById('nameError');
    if (this.value && !validateName(this.value)) {
        nameError.textContent = 'Name must be at least 2 characters';
        this.classList.add('error');
    } else {
        nameError.textContent = '';
        this.classList.remove('error');
    }
});

emailInput.addEventListener('blur', function() {
    const emailError = document.getElementById('emailError');
    if (this.value && !validateEmail(this.value)) {
        emailError.textContent = 'Please enter a valid Gmail address (@gmail.com)';
        this.classList.add('error');
    } else {
        emailError.textContent = '';
        this.classList.remove('error');
    }
});

passwordInput.addEventListener('input', function() {
    const passwordError = document.getElementById('passwordError');
    if (this.value && !validatePassword(this.value)) {
        passwordError.textContent = `${this.value.length}/8 characters (minimum 8 required)`;
        this.classList.add('error');
    } else if (this.value) {
        passwordError.textContent = '✓ Strong password';
        passwordError.style.color = '#27ae60';
        this.classList.remove('error');
    } else {
        passwordError.textContent = '';
        this.classList.remove('error');
    }
});

confirmPasswordInput.addEventListener('blur', function() {
    const confirmPasswordError = document.getElementById('confirmPasswordError');
    if (this.value && this.value !== passwordInput.value) {
        confirmPasswordError.textContent = 'Passwords do not match';
        this.classList.add('error');
    } else {
        confirmPasswordError.textContent = '';
        this.classList.remove('error');
    }
});

// Form submission
signupForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    hideMessages();
    
    const fullName = fullNameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    
    // Validate all fields
    if (!validateName(fullName)) {
        showError('Please enter your full name (at least 2 characters)');
        fullNameInput.focus();
        return;
    }
    
    if (!validateEmail(email)) {
        showError('Please enter a valid Gmail address (@gmail.com)');
        emailInput.focus();
        return;
    }
    
    if (!validatePassword(password)) {
        showError('Password must be at least 8 characters');
        passwordInput.focus();
        return;
    }
    
    if (password !== confirmPassword) {
        showError('Passwords do not match');
        confirmPasswordInput.focus();
        return;
    }
    
    // Show loading state
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.querySelector('.btn-loader');
    const submitBtn = signupForm.querySelector('button[type="submit"]');
    
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    submitBtn.disabled = true;
    
    try {
        // Send signup request to backend
        const response = await fetch('http://localhost:5000/api/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                email, 
                password, 
                full_name: fullName 
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showSuccess('Account created successfully! Redirecting to login...');
            
            // Clear form
            signupForm.reset();
            
            // Redirect to login after 2 seconds
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            showError(data.error || 'Unable to create account. Please try again.');
            btnText.style.display = 'inline-block';
            btnLoader.style.display = 'none';
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Signup error:', error);
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
        window.location.href = 'index.html';
    }
});
