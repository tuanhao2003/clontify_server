const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const BASE_URL = 'http://localhost:8083/storage';

async function testUploadFile() {
    try {
        // Test case 1: Upload MP3 file
        console.log('Test case 1: Upload MP3 file');
        const formData1 = new FormData();
        formData1.append('file', fs.createReadStream('./test_files/test.mp3'));
        
        const response1 = await axios.post(`${BASE_URL}/upload`, formData1, {
            headers: {
                ...formData1.getHeaders()
            }
        });
        console.log('MP3 Upload Response:', response1.data);
        
        // Test case 2: Upload MP4 file
        console.log('\nTest case 2: Upload MP4 file');
        const formData2 = new FormData();
        formData2.append('file', fs.createReadStream('./test_files/test.mp4'));
        
        const response2 = await axios.post(`${BASE_URL}/upload`, formData2, {
            headers: {
                ...formData2.getHeaders()
            }
        });
        console.log('MP4 Upload Response:', response2.data);
        
        // Test case 3: Upload invalid file type
        console.log('\nTest case 3: Upload invalid file type');
        const formData3 = new FormData();
        formData3.append('file', fs.createReadStream('./test_files/test.jpg'));
        
        try {
            const response3 = await axios.post(`${BASE_URL}/upload`, formData3, {
                headers: {
                    ...formData3.getHeaders()
                }
            });
            console.log('Invalid file type Response:', response3.data);
        } catch (error) {
            console.log('Expected error for invalid file type:', error.response.data);
        }
        
    } catch (error) {
        console.error('Test failed:', error.message);
    }
}

testUploadFile(); 