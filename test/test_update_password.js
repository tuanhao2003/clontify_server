// Hàm đổi mật khẩu (giống file test_update_password.js)
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

// Hàm lấy email và kiểm tra password
const getEmailByAccountID = async (accountID, currentPassword) => {
    // Lấy CSRF token từ cookie
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

    try {
        // 1. Lấy email từ accountID
        const response = await fetch('http://localhost:8080/account/find', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'Authorization': `Bearer ${accessToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ id: accountID })
        });

        const result = await response.json();
        if (result && result.data && result.data.email) {
            const email = result.data.email;
            console.log('Email:', email);

            // 2. Gọi API login để kiểm tra password hiện tại
            const loginRes = await fetch('http://localhost:8080/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                credentials: 'include',
                body: JSON.stringify({ email, password: currentPassword })
            });
            const loginResult = await loginRes.json();
            if (loginResult && loginResult.success) {
                console.log('Đăng nhập thành công, tiến hành đổi mật khẩu...');
                // 3. Gọi hàm đổi mật khẩu
                testUpdatePassword();
            } else {
                console.log('Sai mật khẩu hiện tại hoặc tài khoản không hợp lệ.');
            }
        } else {
            console.log('Không tìm thấy email hoặc tài khoản.');
        }
    } catch (error) {
        console.error('Lỗi:', error);
    }
};

// Sử dụng:
const accountId = localStorage.getItem('account_id');
const currentPassword = prompt("Nhập mật khẩu hiện tại:");
getEmailByAccountID(accountId, currentPassword);