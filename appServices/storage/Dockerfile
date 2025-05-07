FROM python:3.12

WORKDIR /storage_service

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN python -m grpc_tools.protoc \
    -I./app/grpc/protos \
    --python_out=./app/grpc/protos \
    --grpc_python_out=./app/grpc/protos \
    ./app/grpc/protos/storageService.proto \
    ./app/grpc/protos/musicService.proto \
    sed -i 's/^import \(.*_pb2\)/from . import \1/' ./app/grpc/protos/*_pb2_grpc.py && \
    sed -i 's/^import \(.*_pb2\)/from . import \1/' ./app/grpc/protos/*_pb2*.py
    
CMD python manage.py makemigrations app && \
    python manage.py migrate app && \
    python manage.py runserver 0.0.0.0:8082