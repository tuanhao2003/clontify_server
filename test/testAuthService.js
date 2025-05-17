// Test file for Auth Controller
const BASE_URL = 'http://localhost:8080';

// Helper function to get CSRF token from cookies
function getCsrfToken() {
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

// Helper function to get access token from localStorage
function getAccessToken() {
    return localStorage.getItem('access_token');
}

// Helper function to make API calls
async function makeRequest(url, method = 'GET', body = null) {
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
        'Authorization': `Bearer ${getAccessToken()}`
    };

    const options = {
        method,
        headers,
        body: body ? JSON.stringify(body) : null,
        credentials: 'include'
    };

    try {
        const response = await fetch(url, options);
        const data = await response.json();
        return { status: response.status, data };
    } catch (error) {
        console.error('Error:', error);
        return { status: 500, data: { error: error.message } };
    }
}

// Test Cases for Auth Controller
async function testAuthController() {
    console.log('Testing Auth Controller...');

    // Test 1: Register new account
    console.log('\nTest 1: Register new account');
    const registerAccount = await makeRequest(`${BASE_URL}/auth/register`, 'POST', {
        username: 'testuser' + Math.floor(Math.random() * 1000),
        email: 'test' + Math.floor(Math.random() * 1000) + '@example.com',
        password: 'Test@123',
        confirmPassword: 'Test@123'
    });
    console.log('Response:', registerAccount);

    // Test 2: Login
    console.log('\nTest 2: Login');
    const login = await makeRequest(`${BASE_URL}/auth/login`, 'POST', {
        username: 'testuser',
        password: 'Test@123'
    });
    console.log('Response:', login);

    // Test 3: Get current user profile
    console.log('\nTest 3: Get current user profile');
    const getProfile = await makeRequest(`${BASE_URL}/auth/profile`);
    console.log('Response:', getProfile);

    // Test 4: Update profile
    console.log('\nTest 4: Update profile');
    const updateProfile = await makeRequest(`${BASE_URL}/auth/profile/update`, 'POST', {
        fullName: 'Test User Updated',
        avatarUrl: 'https://example.com/avatar.jpg',
        bio: 'This is an updated bio',
        dateOfBirth: '1990-01-01',
        phoneNumber: '1234567890'
    });
    console.log('Response:', updateProfile);

    // Test 5: Refresh token
    console.log('\nTest 5: Refresh token');
    const refreshToken = await makeRequest(`${BASE_URL}/auth/refresh`, 'POST', {
        refresh: localStorage.getItem('refresh_token')
    });
    console.log('Response:', refreshToken);

    // Test 6: Change password
    console.log('\nTest 6: Change password');
    const changePassword = await makeRequest(`${BASE_URL}/auth/change-password`, 'POST', {
        oldPassword: 'Test@123',
        newPassword: 'NewTest@123',
        confirmPassword: 'NewTest@123'
    });
    console.log('Response:', changePassword);

    // Test 7: Logout
    console.log('\nTest 7: Logout');
    const logout = await makeRequest(`${BASE_URL}/auth/logout`, 'POST');
    console.log('Response:', logout);
}

// Run all tests
testAuthController().catch(console.error); 