// Authentication Check - Include this in all protected pages
// Add this script at the top of every page that requires authentication

(function() {
    // List of public pages that don't require authentication
    const publicPages = ['login.html', 'signup.html'];
    const currentPage = window.location.pathname.split('/').pop();
    
    // If this is a public page, skip auth check
    if (publicPages.includes(currentPage)) {
        return;
    }
    
    // Check if user is authenticated
    const authToken = localStorage.getItem('authToken');
    
    if (!authToken) {
        // Not authenticated, redirect to login
        window.location.href = 'login.html';
        return;
    }
    
    // Verify token with server
    fetch('http://localhost:5000/api/auth/verify', {
        headers: {
            'Authorization': `Bearer ${authToken}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            // Token invalid, clear and redirect to login
            localStorage.removeItem('authToken');
            localStorage.removeItem('userEmail');
            localStorage.removeItem('userName');
            window.location.href = 'login.html';
        } else {
            // Token valid, user is authenticated
            // Display user info in header if available
            const userName = localStorage.getItem('userName');
            const userEmail = localStorage.getItem('userEmail');
            
            // Add user info to header if element exists
            const userInfoElement = document.getElementById('userInfo');
            if (userInfoElement && userName) {
                userInfoElement.innerHTML = `
                    <div class="user-profile">
                        <span class="user-name">${userName}</span>
                        <span class="user-email">${userEmail}</span>
                        <button onclick="logout()" class="btn-logout">Logout</button>
                    </div>
                `;
            }
        }
    })
    .catch(error => {
        console.error('Auth verification error:', error);
        // On error, redirect to login for safety
        localStorage.removeItem('authToken');
        window.location.href = 'login.html';
    });
})();

// Logout function
function logout() {
    const authToken = localStorage.getItem('authToken');
    
    // Call logout API
    fetch('http://localhost:5000/api/auth/logout', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${authToken}`
        }
    })
    .finally(() => {
        // Clear local storage
        localStorage.removeItem('authToken');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userName');
        
        // Redirect to login
        window.location.href = 'login.html';
    });
}

// Add Authorization header to all API requests
const originalFetch = window.fetch;
window.fetch = function(url, options = {}) {
    // Only add auth header for API requests
    if (url.includes('/api/') && !url.includes('/api/auth/')) {
        const authToken = localStorage.getItem('authToken');
        if (authToken) {
            options.headers = options.headers || {};
            options.headers['Authorization'] = `Bearer ${authToken}`;
        }
    }
    return originalFetch(url, options);
};
