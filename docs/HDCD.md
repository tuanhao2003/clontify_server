# Hướng dẫn tạo service
## Tạo một folder trong appServices, đặt tên service tương ứng
## Trong cmd, di chuyển vào thư mục này và nhập lệnh `django-admin startproject config .` và `django-admin startapp app`
## Vào folder app tạo thêm 5 folder: `controllers`, `entities`, `repositories`, `services` và `serializers`
## Copy `requirement.txt` và `Dockerfile` trong `baseSetup` vào thư mục chính của service, sửa lại thông tin cho phù hợp, quan trọng phải sửa port
## Đăng ký service trong `docker-compose.yml`
---
# Hướng dẫn cấu hình service
## Vào /database/init.sql thêm `CREATE DATABASE tên service;`
## Vào file `setting` config các mục sau: `SECRET_KEY`(giống authservice), `INSTALLED_APPS`, `MIDDLEWARE`, `DATABASES`, `REST_FRAMEWORK`, `SIMPLE_JWT` và các config cors, csrf như authservice
## Vào thư mục `entities`, tạo các file entity đại diện cho các bảng trong db
## Viết repo, service, controller
## Import các file repo vào file `models.py`
## Viết file `urls.py`
---
# Hướng dẫn cấu hình gRPC
## python -m grpc_tools.protoc .\app\grpc\protos\userService.proto --python_out=./app/grpc/protos --grpc_python_out=./app/grpc/protos --proto_path=./app/grpc/protos