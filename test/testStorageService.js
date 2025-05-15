// Test Storage Service
const BASE_URL = 'http://localhost:8083'; // Change this to your actual base URL

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
async function testGetStorageData(page = 1, pageSize = 10) {
    console.log('Testing Get Storage Data...');
    const response = await makeRequest(`/storages?page=${page}&pageSize=${pageSize}`);
    console.log('Response:', response);
    return response;
}

async function testGetStorageDataById(id) {
    console.log('Testing Get Storage Data By ID...');
    const response = await makeRequest(`/storage/${id}`);
    console.log('Response:', response);
    return response;
}

async function testCreateStorageData(data) {
    console.log('Testing Create Storage Data...');
    const response = await makeRequest('/storage/create', 'POST', data);
    console.log('Response:', response);
    return response;
}

async function testUpdateStorageData(data) {
    console.log('Testing Update Storage Data...');
    const response = await makeRequest('/storage/update', 'POST', data);
    console.log('Response:', response);
    return response;
}

async function testDeleteStorageData(id) {
    console.log('Testing Delete Storage Data...');
    const response = await makeRequest('/storage/delete', 'POST', { id });
    console.log('Response:', response);
    return response;
}

// File upload function
async function testUploadFile(file, fileType, fileName) {
    console.log('Testing Upload File...');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileType', fileType);
    formData.append('fileName', fileName);
    const headers = {
        'X-CSRFToken': getCSRFToken(),
        'Authorization': `Bearer ${getAuthToken()}`
    };

    try {
        const response = await fetch(`${BASE_URL}/storage/upload`, {
            method: 'POST',
            headers,
            body: formData,
            credentials: 'include'
        });
        const result = await response.json();
        console.log('Response:', result);
        return result;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Example usage:
// 1. Get all storage data
// testGetStorageData();

// 2. Get storage data by ID
// testGetStorageDataById('8c37e119-06af-485d-96f7-ff53870de2da');

// 3. Create storage data
// testCreateStorageData({
//     fileName: '0bcc61a6-e3bf-4ef7-896d-264ab62f4b2c.mp3',
//     fileType: 'audio/mpeg',
//     userId: localStorage.getItem('account_id'),
//     fileUrl: 'https://clontify-storage.s3.ap-southeast-2.amazonaws.com/0bcc61a6-e3bf-4ef7-896d-264ab62f4b2c.mp3',
//     fileSize: 409964,
//     description: 'Test file'
// });

// 4. Update storage data
// testUpdateStorageData({
//     id: '8c37e119-06af-485d-96f7-ff53870de2da',
//     fileName: 'updated.mp3',
//     fileType: 'audio/mpeg',
//     fileSize: 409964,
//     fileUrl: 'https://clontify-storage.s3.ap-southeast-2.amazonaws.com/0bcc61a6-e3bf-4ef7-896d-264ab62f4b2c.mp3',
//     description: 'Updated test file'
// });

// 5. Delete storage data
testDeleteStorageData('8c37e119-06af-485d-96f7-ff53870de2da');

// 6. Upload file
// const fileInput = document.createElement('input');
// fileInput.type = 'file';
// fileInput.accept = 'audio/mpeg,video/mp4';
// fileInput.onchange = (e) => {
//     const file = e.target.files[0];
//     if (file) {
//         testUploadFile(file, 'AUDIO', 'test.mp3');
//     }
// };
// fileInput.click();