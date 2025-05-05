const testUpdatePassword = async () => {
    const newPassword = "newPassword123";

    const getCookie = (name) => {
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
    };

    const csrftoken = getCookie('csrftoken');
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        console.error('Không tìm thấy access token. Vui lòng đăng nhập trước!');
        return;
    }

    const data = {
        password: newPassword
    };

    try {
        const response = await fetch('http://localhost:8080/account/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'Authorization': `Bearer ${accessToken}`
            },
            credentials: 'include',
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log('Kết quả:', result);
    } catch (error) {
        console.error('Lỗi:', error);
    }
};

testUpdatePassword(); 