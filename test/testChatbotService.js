// Test Storage Service
const BASE_URL = 'http://localhost:8084'; // Change this to your actual base URL

// Helper function to get CSRF token from cookies
function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper function to get authorization token from localStorage
function getAuthToken() {
    return localStorage.getItem('access_token');
}

// Helper function to make API calls
async function makeRequest(endpoint, method = 'GET', data = null) {
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
        'Authorization': `Bearer ${getAuthToken()}`
    };
    
    const options = {
        method,
        headers,
        credentials: 'include'
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Test functions
async function testAsk(data) {
    console.log('Testing ask...');
    const response = await makeRequest('/ask', 'POST', data);
    console.log('Response:', response);
    return response;
}

// Example usage:

testAsk({
    prompt: "nói tiếng việt đi"
});