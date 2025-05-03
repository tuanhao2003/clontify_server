async function testRegister() {
    const registerData = {
        username: "admin",
        email: "admin@example.com",
        password: "admin",
        fullName: "test user",
        avatarUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8WOsLxlKgTXh7gry1qONjjpnozv1IwdHf165tgttVd5FiaWx4G8yOo4LCWt9uPt6y0EWxE89oyHdEPbgre41s8Q",
        bio: "I am the first user",
        dateOfBirth: "1990-01-01",
        phoneNumber: "0123456788"
    };

    try {
        const response = await fetch('http://localhost:8080/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': await getCsrfToken()
            },
            body: JSON.stringify(registerData)
        });

        const data = await response.json();
        console.log('Registration Response:', data);
        
        if (response.ok) {
            console.log('Registration successful!');
            console.log('Data:', data.data);

        } else {
            console.error('Registration failed:', data.message);
        }
    } catch (error) {
        console.error('Error during registration:', error);
    }
}

async function getCsrfToken() {
    try {
        const response = await fetch('http://localhost:8080/csrf', {
            method: 'GET',
            credentials: 'include'
        });
        const data = await response.json();
        return data.data.token;
    } catch (error) {
        console.error('Error getting CSRF token:', error);
        return null;
    }
}

testRegister(); 