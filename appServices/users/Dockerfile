FROM python:3.12

WORKDIR /users_service

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# COPY . .

CMD if [ "$BUILD_PROTO" != "0" ]; then \
        python -m grpc_tools.protoc -I./app/grpc/protos --python_out=./app/grpc/protos --grpc_python_out=./app/grpc/protos ./app/grpc/protos/authService.proto ./app/grpc/protos/usersService.proto && \
        sed -i 's/^import \(.*_pb2\)/from . import \1/' ./app/grpc/protos/*_pb2_grpc.py && \
        sed -i 's/^import \(.*_pb2\)/from . import \1/' ./app/grpc/protos/*_pb2*.py; \
    fi && \
    if [ "$RUN_MIGRATIONS" != "0" ]; then \
        python manage.py makemigrations app && \
        python manage.py migrate app; \
    fi && \
    python manage.py runserver 0.0.0.0:8081
