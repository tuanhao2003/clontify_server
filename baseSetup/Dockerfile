FROM python:3.12

WORKDIR /auth_service

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD python -m grpc_tools.protoc ./app/grpc/protos/authService.proto --python_out=./app/grpc/protos --grpc_python_out=./app/grpc/protos --proto_path=./app/grpc/protos && \
    python manage.py makemigrations app && \
    python manage.py migrate app && \
    python manage.py runserver 0.0.0.0:8081 && \
    python ./app/grpc/grpcServers/authGrpc.py
