const axios = require('axios');

const BASE_URL = 'http://localhost:8083/storage';

// Store created storage data ID for testing
let createdStorageId;

async function testCreateStorageData() {
    try {
        console.log('Test case 1: Create storage data');
        const createData = {
            fileName: "test_file.mp3",
            fileType: "audio/mpeg",
            userId: "123e4567-e89b-12d3-a456-426614174000", // Replace with valid UUID
            fileUrl: "https://example.com/test.mp3",
            fileSize: 1024,
            description: "Test file description"
        };

        const response = await axios.post(`${BASE_URL}/create`, createData);
        console.log('Create Response:', response.data);
        createdStorageId = response.data.data.id;
    } catch (error) {
        console.error('Create test failed:', error.response?.data || error.message);
    }
}

async function testGetStorageData() {
    try {
        // Test case 1: Get all storage data
        console.log('\nTest case 1: Get all storage data');
        const response1 = await axios.get(`${BASE_URL}?page=1&pageSize=10`);
        console.log('Get All Response:', response1.data);

        // Test case 2: Get storage data by ID
        if (createdStorageId) {
            console.log('\nTest case 2: Get storage data by ID');
            const response2 = await axios.get(`${BASE_URL}/${createdStorageId}`);
            console.log('Get By ID Response:', response2.data);
        }
    } catch (error) {
        console.error('Get test failed:', error.response?.data || error.message);
    }
}

async function testUpdateStorageData() {
    try {
        if (!createdStorageId) {
            console.log('No storage data ID available for update test');
            return;
        }

        console.log('\nTest case: Update storage data');
        const updateData = {
            id: createdStorageId,
            fileName: "updated_file.mp3",
            fileType: "audio/mpeg",
            fileSize: 2048,
            fileUrl: "https://example.com/updated.mp3"
        };

        const response = await axios.post(`${BASE_URL}/update`, updateData);
        console.log('Update Response:', response.data);
    } catch (error) {
        console.error('Update test failed:', error.response?.data || error.message);
    }
}

async function testDeleteStorageData() {
    try {
        if (!createdStorageId) {
            console.log('No storage data ID available for delete test');
            return;
        }

        console.log('\nTest case: Delete storage data');
        const deleteData = {
            id: createdStorageId
        };

        const response = await axios.post(`${BASE_URL}/delete`, deleteData);
        console.log('Delete Response:', response.data);
    } catch (error) {
        console.error('Delete test failed:', error.response?.data || error.message);
    }
}

async function runTests() {
    await testCreateStorageData();
    await testGetStorageData();
    await testUpdateStorageData();
    await testDeleteStorageData();
}

runTests(); 