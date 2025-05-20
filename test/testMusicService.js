// Test file for Songs Controller
const BASE_URL = 'http://localhost:8082';

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

// test albums
async function testAlbumsController() {
    console.log('Testing Albums Controller...');
    const albumId = "75d14f62-dd62-47bf-9c7d-d68671abd824"; // Valid UUID format

    // Test 1: Get all albums (paginated)
    // console.log('\nTest 1: Get all albums');
    // const getAllAlbums = await makeRequest(`${BASE_URL}/albums?page=1&pageSize=10`);
    // console.log('Response:', getAllAlbums);

    // Test 2: Get album by ID
    // console.log('\nTest 2: Get album by ID');
    // try {
    //     const getAlbumById = await makeRequest(`${BASE_URL}/album/${albumId}`);
    //     console.log('Response:', getAlbumById);
    //     if (getAlbumById.status !== 200) {
    //         console.error('Error details:', getAlbumById.data);
    //     }
    // } catch (error) {
    //     console.error('Error fetching album:', error);
    // }

    // Test 3: Search albums by name
    // console.log('\nTest 3: Search albums by name');
    // const searchByName = await makeRequest(`${BASE_URL}/albums`, 'POST', {
    //     name: 'Test Album',
    //     page: 1,
    //     pageSize: 10
    // });
    // console.log('Response:', searchByName);

    // Test 4: Create new album
    console.log('\nTest 4: Create new album');
    const accountId = localStorage.getItem('account_id');
    const createAlbum = await makeRequest(`${BASE_URL}/album/create`, 'POST', {
        name: 'New Test Album',
        description: 'Test album description',
        storageImageId: crypto.randomUUID(),
        artistId: accountId
    });
    console.log('Response:', createAlbum);

    // Test 5: Update album
    // console.log('\nTest 5: Update album');
    // const updateAlbum = await makeRequest(`${BASE_URL}/album/update`, 'POST', {
    //     id: albumId,
    //     name: 'hahahaa',
    //     description: 'ngu quá mày',
    //     storageImageId: crypto.randomUUID(),
    // });
    // console.log('Response:', updateAlbum);

    // Test 6: Delete album
    // console.log('\nTest 6: Delete album');
    // const deleteAlbum = await makeRequest(`${BASE_URL}/album/delete`, 'POST', {
    //     id: "fc9debe5-3085-4346-8f71-e49e69ec41fc"
    // });
    // console.log('Response:', deleteAlbum);
}
// Run all tests
testAlbumsController().catch(console.error);





// Test Cases for Genres Controller
async function testGenresController() {
    console.log('Testing Genres Controller...');
    const genreId = '8fd250dd-1fcb-470a-973c-22d942e7496d'; // Replace with actual genre ID

    // // Test 1: Get all genres (paginated)
    // console.log('\nTest 1: Get all genres');
    // const getAllGenres = await makeRequest(`${BASE_URL}/genres?page=1&pageSize=10`);
    // console.log('Response:', getAllGenres);

    // // Test 2: Get genre by ID
    // console.log('\nTest 2: Get genre by ID');
    // const getGenreById = await makeRequest(`${BASE_URL}/genre/${genreId}`);
    // console.log('Response:', getGenreById);

    // // Test 3: Search genres by name
    // console.log('\nTest 3: Search genres by name');
    // const searchByName = await makeRequest(`${BASE_URL}/genres`, 'POST', {
    //     name: 'Test Genre',
    //     page: 1,
    //     pageSize: 10
    // });
    // console.log('Response:', searchByName);

    // // Test 4: Get genres by song ID
    // console.log('\nTest 4: Get genres by song ID');
    // const getGenresBySong = await makeRequest(`${BASE_URL}/genres`, 'POST', {
    //     songId: '1', // Replace with actual song ID
    //     page: 1,
    //     pageSize: 10
    // });
    // console.log('Response:', getGenresBySong);

    // // Test 5: Create new genre
    // console.log('\nTest 5: Create new genre');
    // const createGenre = await makeRequest(`${BASE_URL}/genre/create`, 'POST', {
    //     name: 'New Test Genre',
    //     description: 'Test genre description'
    // });
    // console.log('Response:', createGenre);

    // // Test 6: Update genre
    // console.log('\nTest 6: Update genre');
    // const updateGenre = await makeRequest(`${BASE_URL}/genre/update`, 'POST', {
    //     id: genreId, // Replace with actual genre ID
    //     name: 'Updated Test Genre',
    //     description: 'Updated test genre description'
    // });
    // console.log('Response:', updateGenre);

    // // Test 7: Delete genre
    // console.log('\nTest 7: Delete genre');
    // const deleteGenre = await makeRequest(`${BASE_URL}/genre/delete`, 'POST', {
    //     id: genreId // Replace with actual genre ID
    // });
    // console.log('Response:', deleteGenre);
}
// Run all tests
testGenresController().catch(console.error); 





// Test Cases for Songs Controller
async function testSongsController() {
    console.log('Testing Songs Controller...');
    const songId = '060b94ed-6102-45e4-bd45-09bd6732fd6a'; // Replace with actual song ID
    const accountId = localStorage.getItem('account_id');

    // // Test 1: Get all songs (paginated)
    // console.log('\nTest 1: Get all songs');
    // const getAllSongs = await makeRequest(`${BASE_URL}/songs`, 'POST', {
    //     page: 1,
    //     pageSize: 10
    // });
    // console.log('Response:', getAllSongs);

    // // Test 2: Get song by ID
    // console.log('\nTest 2: Get song by ID');
    // const getSongById = await makeRequest(`${BASE_URL}/song/${songId}`);
    // console.log('Response:', getSongById);

    // // Test 3: Search songs by title
    // console.log('\nTest 3: Search songs by title');
    // const searchByTitle = await makeRequest(`${BASE_URL}/songs`, 'POST', {
    //     title: 'Test Song',
    //     page: 1,
    //     pageSize: 10
    // });
    // console.log('Response:', searchByTitle);

    // // Test 4: Search songs by artist
    // console.log('\nTest 4: Search songs by artist');
    // const searchByArtist = await makeRequest(`${BASE_URL}/songs`, 'POST', {
    //     artistId: accountId, // Replace with actual artist ID
    //     page: 1,
    //     pageSize: 10
    // });
    // console.log('Response:', searchByArtist);

    // Test 5: Create new song
    // console.log('\nTest 5: Create new song');
    // const createSong = await makeRequest(`${BASE_URL}/song/create`, 'POST', {
    //     title: 'New Test Song',
    //     artistId: accountId,
    //     genreId: ["8fd250dd-1fcb-470a-973c-22d942e7496d"],
    //     storageId: crypto.randomUUID(),
    //     storageImageId: crypto.randomUUID(),
    //     duration: 180,
    //     description: 'Test song description',
    //     albumId: ["75d14f62-dd62-47bf-9c7d-d68671abd824"],
    //     songType: 'SONG'
    // });
    // console.log('Response:', createSong);

    // // Test 6: Update song
    // console.log('\nTest 6: Update song');
    // const updateSong = await makeRequest(`${BASE_URL}/song/update`, 'POST', {
    //     id: songId, // Replace with actual song ID
    //     title: 'go to disney',
    //     storageImageId: crypto.randomUUID(), // Replace with actual image ID
    //     duration: 200,
    //     description: 'new desc',
    //     songType: 'MUSIC_VIDEO'
    // });
    // console.log('Response:', updateSong);

    // // Test 7: Delete song
    // console.log('\nTest 7: Delete song');
    // const deleteSong = await makeRequest(`${BASE_URL}/song/delete`, 'POST', {
    //     id: songId // Replace with actual song ID
    // });
    // console.log('Response:', deleteSong);
}
// Run all tests
testSongsController().catch(console.error); 