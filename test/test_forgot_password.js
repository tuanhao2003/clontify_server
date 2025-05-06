// Hàm lấy CSRF token từ cookie
function getCookie(name) {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1] || null;
}

// Hàm kiểm tra email có tồn tại không
async function checkEmailExists(email, csrftoken) {
    try {
        const response = await fetch('http://localhost:8080/account/find', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
            body: JSON.stringify({ email })
        });
        const result = await response.json();
        return result.success;
    } catch (error) {
        console.error("Lỗi khi kiểm tra email:", error);
        return false;
    }
}

// Hàm test quên mật khẩu
async function testForgotPassword() {
    const email = prompt("Nhập email cần đặt lại mật khẩu:");
    if (!email) {
        console.error("Vui lòng nhập email!");
        return;
    }

    const csrftoken = getCookie('csrftoken');

    // Bước 0: Kiểm tra email có tồn tại không
    console.log("Đang kiểm tra email...");
    const exists = await checkEmailExists(email, csrftoken);
    if (!exists) {
        console.error("Email không tồn tại trong hệ thống!");
        return;
    }
    console.log("Email hợp lệ, tiếp tục quên mật khẩu...");

    try {
        // Bước 1: Yêu cầu đặt lại mật khẩu
        console.log("Đang gửi yêu cầu đặt lại mật khẩu...");
        const requestResponse = await fetch('http://localhost:8080/password-reset/request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
            body: JSON.stringify({ email })
        });

        const requestResult = await requestResponse.json();
        console.log("Kết quả yêu cầu:", requestResult);

        if (!requestResult.success) {
            console.error("Lỗi:", requestResult.message);
            return;
        }

        // Lưu token để sử dụng ở bước tiếp theo
        const token = requestResult.data.token;
        console.log("Token nhận được:", token);

        // Bước 2: Nhập mã xác thực và mật khẩu mới
        const verificationCode = prompt("Nhập mã xác thực từ email:");
        if (!verificationCode) {
            console.error("Vui lòng nhập mã xác thực!");
            return;
        }

        const newPassword = prompt("Nhập mật khẩu mới:");
        if (!newPassword) {
            console.error("Vui lòng nhập mật khẩu mới!");
            return;
        }

        // Bước 3: Xác thực và đặt lại mật khẩu
        console.log("Đang xác thực và đặt lại mật khẩu...");
        const verifyResponse = await fetch('http://localhost:8080/password-reset/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
            body: JSON.stringify({
                token,
                verification_code: verificationCode,
                new_password: newPassword
            })
        });

        const verifyResult = await verifyResponse.json();
        console.log("Kết quả xác thực:", verifyResult);

        if (verifyResult.success) {
            console.log("Đặt lại mật khẩu thành công!");
        } else {
            console.error("Lỗi:", verifyResult.message);
        }

    } catch (error) {
        console.error("Lỗi:", error);
    }
}

// Chạy test
testForgotPassword();