# Lưu ý: dự án này sẽ không phân nhánh như dự án trước mà sẽ có cấu trúc như sau:
  - Nhánh main như mọi lần
  - Các nhánh feature/* => chức năng đang phát triển
  - Các nhánh bugfix/* => sửa bug

# Quy tắc dùng git:    
1/ Luôn luôn pull code mới nhất từ nhánh main khi bắt đầu làm
2/ Khi nhận task, từ nhánh main tạo 1 nhánh mới có tên là feature/... hoặc bugfix/... dựa theo chức năng của task đó (dùng git checkout -b tên)
3/ Code trên nhánh vừa tạo, khi code xong commit như bình thường (nếu muốn chuẩn thì trong message của commit ghi thêm chức năng task như "feat:...", "fix:..." hoặc "refactor:...")
4/ Sau khi push lên, vào github để tạo pull request
5/ Báo t để merge