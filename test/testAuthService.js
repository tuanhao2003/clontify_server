// Test Storage Service
const BASE_URL = 'http://localhost:8080'; // Change this to your actual base URL

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
async function testGetRoles(data) {
    console.log('Testing Favorite...');
    const response = await makeRequest('/roles', 'POST', data);
    console.log('Response:', response);
    return response;
}
async function testCreateRoles(data) {
    console.log('Testing Favorite...');
    const response = await makeRequest('/role/create', 'POST', data);
    console.log('Response:', response);
    return response;
}
async function testDeleteRoles(data) {
    console.log('Testing Favorite...');
    const response = await makeRequest('/role/delete', 'POST', data);
    console.log('Response:', response);
    return response;
}

// Example usage:
// testGetRoles({
//     name: "ADMIN",
//     page: 1,
//     pageSize:10
// });

// testCreateRoles({
//     name: "MMSB",
//     description: "no cap"
// });

testDeleteRoles({
    ids: ["5d6e3c44-cce3-470b-8a01-3b44894940e5","6d6e3c44-cce3-470b-8a01-3b44894940e5"]
});