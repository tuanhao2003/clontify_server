# pgAdmin Setup Guide

## English Version

### Accessing pgAdmin Site

1. Open a web browser and navigate to `http://localhost:5050`.
2. Log in using the provided credentials:
    - **Username:** admin@clontify.com
    - **Password:** admin
      ![pgadmin login](images/pgadmin-login.png)

### Adding the Database Server

1. Click on **"Add New Server"** in the pgAdmin dashboard.
   ![pgadmin add new server](images/pgadmin-add-new-server.png)
2. In the **General** tab, fill in:
    - **Name:** postgres
      ![pgadmin add new server general tab](images/pgadmin-add-new-server-general-tab.png)

### Configuring the Connection

1. Go to the **Connection** tab.
2. Enter the following values:

    - **Host name/address:** postgres
    - **Port:** 5432
    - **Maintenance database:** postgres
    - **Username:** admin
    - **Password:** admin
      ![pgadmin add new server connection tab](images/pgadmin-add-new-server-connection-tab.png)

3. Keep other fields as default and click **Save**.

### Testing the Connection

1. After saving, the server should appear in the left sidebar.
2. Click on the server name to expand it.
3. If successful, databases will be listed under the server.
   ![pgadmin add new server success](images/pgadmin-add-new-server-success.png)

---

## Vietnamese Version

### Truy cập trang pgAdmin

1. Mở trình duyệt web và truy cập `http://localhost:5050`.
2. Đăng nhập bằng thông tin sau:
    - **Tên đăng nhập:** admin@clontify.com
    - **Mật khẩu:** admin
      ![pgadmin login](images/pgadmin-login.png)

### Thêm máy chủ cơ sở dữ liệu

1. Nhấp vào **"Add New Server"** trên bảng điều khiển pgAdmin.
2. Trong tab **General**, nhập:
    - **Tên:** postgres
      ![pgadmin add new server general tab](images/pgadmin-add-new-server-general-tab.png)

### Cấu hình kết nối

1. Chuyển sang tab **Connection**.
2. Điền các trường với thông tin sau:

    - **Host name/address:** postgres
    - **Port:** 5432
    - **Maintenance database:** postgres
    - **Tên đăng nhập:** admin
    - **Mật khẩu:** admin
      ![pgadmin add new server connection tab](images/pgadmin-add-new-server-connection-tab.png)

3. Giữ nguyên các trường khác và nhấp **Save**.

### Kiểm tra kết nối

1. Sau khi lưu, máy chủ sẽ xuất hiện ở thanh bên trái.
2. Nhấp vào tên máy chủ để mở rộng.
3. Nếu kết nối thành công, bạn sẽ thấy danh sách cơ sở dữ liệu dưới máy chủ.
   ![pgadmin add new server success](images/pgadmin-add-new-server-success.png)

# Database Backup and Restore Guide

## English Version

### Backup Process

1. Open pgAdmin and navigate to the PostgreSQL server.
2. Right-click on the server and select **Backup**.
   ![pgadmin backup server](images/pgadmin-backup-server.png)
3. In the **General** tab:
    - Set **File Name** to `serverclontify.sql`.
    - Set **Role** to `admin`.
      ![pgadmin backup server general tab](images/pgadmin-backup-server-general-tab.png)
4. Go to the **Query Options** tab.
    - Ensure the settings match the following:
        - **Use INSERT Commands:** Disabled
        - **Maximum rows per INSERT command:** Leave empty
        - **On conflict do nothing to INSERT command:** Disabled
        - **Include DROP DATABASE statement:** Enabled
        - **Include IF EXISTS clause:** Enabled
          ![pgadmin backup server query options tab](images/pgadmin-backup-server-query-options-tab.png)
5. Click **Backup** to generate the file.
   ![pgadmin backup server success](images/pgadmin-backup-server-success.png)
6. Move the backup file `serverclontify.sql` to the root directory of the backend server (`clontify-server`).
   ![pgadmin backup server move file](images/pgadmin-backup-server-move-file.png)

### Restore Process

1. Open Docker Desktop and select the PostgreSQL container.
   ![docker desktop restore server](images/docker-desktop-restore-server.png)
2. Navigate to the **Exec** tab.

3. Run the following command:
    ```sh
    psql -U admin -X -f /serverclontify.sql -d postgres
    ```
    ![docker desktop restore server command](images/docker-desktop-restore-server-command.png)
4. Wait for the process to complete. The database is now restored.
   ![docker desktop restore server success](images/docker-desktop-restore-server-success.png)

---

## Vietnamese Version

### Quá trình sao lưu

1. Mở pgAdmin và điều hướng đến máy chủ PostgreSQL.
2. Nhấp chuột phải vào máy chủ và chọn **Backup**.
   ![pgadmin backup server](images/pgadmin-backup-server.png)

3. Trong tab **General**:

    - Đặt **File Name** là `serverclontify.sql`.
    - Đặt **Role** là `admin`.
      ![pgadmin backup server general tab](images/pgadmin-backup-server-general-tab.png)

4. Chuyển sang tab **Query Options**.

    - Đảm bảo các cài đặt sau:
        - **Use INSERT Commands:** Tắt
        - **Maximum rows per INSERT command:** Để trống
        - **On conflict do nothing to INSERT command:** Tắt
        - **Include DROP DATABASE statement:** Bật
        - **Include IF EXISTS clause:** Bật
          ![pgadmin backup server query options tab](images/pgadmin-backup-server-query-options-tab.png)

5. Nhấn **Backup** để tạo tập tin sao lưu.
   ![pgadmin backup server success](images/pgadmin-backup-server-success.png)
6. Chuyển tập tin sao lưu `serverclontify.sql` vào thư mục gốc của máy chủ backend (`clontify-server`).
   ![pgadmin backup server move file](images/pgadmin-backup-server-move-file.png)

### Quá trình khôi phục

1.  Mở Docker Desktop và chọn container PostgreSQL.
2.  Chuyển đến tab **Exec**.
    ![docker desktop restore server](images/docker-desktop-restore-server.png)

3.  Chạy lệnh sau:

    ```sh
    psql -U admin -X -f /serverclontify.sql -d postgres
    ```

    ![docker desktop restore server command](images/docker-desktop-restore-server-command.png)

4.  Chờ quá trình hoàn tất. Cơ sở dữ liệu đã được khôi phục.
    ![docker desktop restore server success](images/docker-desktop-restore-server-success.png)
