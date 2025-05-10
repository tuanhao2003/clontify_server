# pgAdmin Setup Guide

## English Version

### Accessing pgAdmin Site
1. Open a web browser and navigate to `http://localhost:5050`.
2. Log in using the provided credentials:
   - **Username:** admin@clontify.com
   - **Password:** admin

### Adding the Database Server
1. Click on **"Add New Server"** in the pgAdmin dashboard.
2. In the **General** tab, fill in:
   - **Name:** postgres

### Configuring the Connection
1. Go to the **Connection** tab.
2. Enter the following values:
   - **Host name/address:** postgres
   - **Port:** 5432
   - **Maintenance database:** postgres
   - **Username:** admin
   - **Password:** admin
3. Keep other fields as default and click **Save**.

### Testing the Connection
1. After saving, the server should appear in the left sidebar.
2. Click on the server name to expand it.
3. If successful, databases will be listed under the server.

---

## Vietnamese Version

### Truy cập trang pgAdmin
1. Mở trình duyệt web và truy cập `http://localhost:5050`.
2. Đăng nhập bằng thông tin sau:
   - **Tên đăng nhập:** admin@clontify.com
   - **Mật khẩu:** admin

### Thêm máy chủ cơ sở dữ liệu
1. Nhấp vào **"Add New Server"** trên bảng điều khiển pgAdmin.
2. Trong tab **General**, nhập:
   - **Tên:** postgres

### Cấu hình kết nối
1. Chuyển sang tab **Connection**.
2. Điền các trường với thông tin sau:
   - **Host name/address:** postgres
   - **Port:** 5432
   - **Maintenance database:** postgres
   - **Tên đăng nhập:** admin
   - **Mật khẩu:** admin
3. Giữ nguyên các trường khác và nhấp **Save**.

### Kiểm tra kết nối
1. Sau khi lưu, máy chủ sẽ xuất hiện ở thanh bên trái.
2. Nhấp vào tên máy chủ để mở rộng.
3. Nếu kết nối thành công, bạn sẽ thấy danh sách cơ sở dữ liệu dưới máy chủ.
