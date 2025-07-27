// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Form validation for scan form
    const scanForm = document.querySelector('.scan-form');
    if (scanForm) {
        scanForm.addEventListener('submit', function(event) {
            const contentField = document.getElementById('content');
            if (!contentField.value.trim()) {
                event.preventDefault();
                alert('Please enter content to scan');
                return false;
            }
            
            // For URL scanning, validate URL format
            const scanType = document.querySelector('input[name="scan_type"]').value;
            if (scanType === 'url' && !isValidURL(contentField.value.trim())) {
                event.preventDefault();
                alert('Please enter a valid URL (e.g., https://example.com)');
                return false;
            }
            
            return true;
        });
    }
    
    // Form validation for login form
    const loginForm = document.querySelector('form[action*="login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            
            if (!username.value.trim() || !password.value.trim()) {
                event.preventDefault();
                alert('Please enter both username and password');
                return false;
            }
            
            return true;
        });
    }
    
    // Form validation for register form
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            const username = document.getElementById('username');
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            const confirmPassword = document.getElementById('confirm_password');
            
            if (!username.value.trim() || !email.value.trim() || !password.value.trim() || !confirmPassword.value.trim()) {
                event.preventDefault();
                alert('Please fill out all fields');
                return false;
            }
            
            if (!isValidEmail(email.value.trim())) {
                event.preventDefault();
                alert('Please enter a valid email address');
                return false;
            }
            
            if (password.value !== confirmPassword.value) {
                event.preventDefault();
                alert('Passwords do not match');
                return false;
            }
            
            if (password.value.length < 8) {
                event.preventDefault();
                alert('Password must be at least 8 characters long');
                return false;
            }
            
            return true;
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(function() {
            alerts.forEach(function(alert) {
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }
    
    // Helper function to validate email format
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // Helper function to validate URL format
    function isValidURL(url) {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    }
});