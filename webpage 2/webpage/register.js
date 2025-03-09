document.getElementById("registerForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    // Get all form values
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const companyName = document.getElementById("companyName").value;
    const companyDescription = document.getElementById("companyDescription").value;
    const products = document.getElementById("products").value.split(',').map(item => item.trim());

    // Password validation
    let passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
    if (!passwordPattern.test(password)) {
        alert("Password must be at least 8 characters long and contain both letters and numbers.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    console.log("sjvkjsfvkjshvkjabvvkajbvbvas");

    try {
        // Prepare request data
        const requestData = {
            username,
            password,
            confirmPassword,
            companyName,
            companyDescription,
            products
        };

        // Make API call
        const response = await fetch('http://localhost:4000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Registration failed');
        }

        const data = await response.json();
        alert("Registration successful!");
        
        // Redirect to login page or dashboard
        window.location.href = '/login.html';

    } catch (error) {
        alert(`Registration failed: ${error.message}`);
        console.error('Registration error:', error);
    }
});

// Optional: Add real-time password matching validation
document.getElementById("confirmPassword").addEventListener("input", function() {
    const password = document.getElementById("password").value;
    const confirmPassword = this.value;
    
    if (password !== confirmPassword) {
        this.setCustomValidity("Passwords don't match");
    } else {
        this.setCustomValidity("");
    }
});