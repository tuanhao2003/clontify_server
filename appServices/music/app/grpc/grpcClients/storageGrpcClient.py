import grpc
from app.grpc.protos import storageService_pb2, storageService_pb2_grpc
from django.conf import settings
from common.errorCodes import ErrorCodes
from google.protobuf import empty_pb2
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

class StorageGrpcClient:
    def __init__(self):
        self.host = getattr(settings, 'STORAGE_GRPC_HOST', 'storage_service')
        self.port = getattr(settings, 'STORAGE_GRPC_PORT', '50053')
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = storageService_pb2_grpc.StorageServiceStub(self.channel)
    
    def close(self):
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None

    def _parseTimestamp(self, dt):
        if not dt or not isinstance(dt, datetime):
            return None
        timestamp = Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp
    
    def _parseDatetime(self, timestamp):
        if not timestamp or not isinstance(timestamp, Timestamp):
            return None
        return timestamp.ToDatetime()

    def _storageSerializer(self, storage):
        return {
            'id': storage.id,
            'userId': storage.userId,
            'fileName': storage.fileName,
            'fileType': storage.fileType,
            'fileSize': storage.fileSize,
            'fileUrl': storage.fileUrl,
            'description': storage.description,
            'createdAt': self._parseDatetime(storage.createdAt),
            'updatedAt': self._parseDatetime(storage.updatedAt),
            'deletedAt': self._parseDatetime(storage.deletedAt),
            'isActive': storage.isActive
        }

    def uploadToS3(self, file_bytes, fileName, fileType):
        try:
            request = storageService_pb2.UploadToS3Request(file=file_bytes, fileName=fileName, fileType=fileType)
            grpcResponse = self.stub.uploadToS3(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return {'key': grpcResponse.key, 'url': grpcResponse.url}, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def findById(self, id):
        try:
            request = storageService_pb2.StringRequest(str=id)
            grpcResponse = self.stub.findById(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._storageSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def findAll(self):
        try:
            grpcResponse = self.stub.findAll(empty_pb2.Empty())
            storages = []
            for storage in grpcResponse:
                storages.append(self._storageSerializer(storage))
            return storages, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def findByIds(self, ids):
        try:
            request = storageService_pb2.ListStringRequest(strs=ids)
            grpcResponse = self.stub.findByIds(request)
            storages = []
            for storage in grpcResponse:
                storages.append(self._storageSerializer(storage))
            return storages, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def findByFileType(self, fileType):
        try:
            request = storageService_pb2.StringRequest(str=fileType)
            grpcResponse = self.stub.findByFileType(request)
            storages = []
            for storage in grpcResponse:
                storages.append(self._storageSerializer(storage))
            return storages, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def findByUserId(self, userId):
        try:
            request = storageService_pb2.StringRequest(str=userId)
            grpcResponse = self.stub.findByUserId(request)
            storages = []
            for storage in grpcResponse:
                storages.append(self._storageSerializer(storage))
            return storages, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def findByFileName(self, fileName):
        try:
            request = storageService_pb2.StringRequest(str=fileName)
            grpcResponse = self.stub.findByFileName(request)
            storages = []
            for storage in grpcResponse:
                storages.append(self._storageSerializer(storage))
            return storages, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def doCreate(self, userId, fileName, fileType, fileSize, fileUrl, description):
        try:
            request = storageService_pb2.CreateRequest(
                userId=userId,
                fileName=fileName,
                fileType=fileType,
                fileSize=fileSize,
                fileUrl=fileUrl,
                description=description
            )
            grpcResponse = self.stub.doCreate(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._storageSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def doUpdate(self, id, fileName=None, fileType=None, fileSize=None, fileUrl=None, description=None):
        try:
            request = storageService_pb2.UpdateRequest(
                id=id,
                fileName=fileName if fileName else '',
                fileType=fileType if fileType else '',
                fileSize=fileSize if fileSize else '',
                fileUrl=fileUrl if fileUrl else '',
                description=description if description else ''
            )
            grpcResponse = self.stub.doUpdate(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._storageSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def doDelete(self, id):
        try:
            request = storageService_pb2.StringRequest(str=id)
            grpcResponse = self.stub.doDelete(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._storageSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def genPublicUrl(self, s3Key):
        try:
            request = storageService_pb2.GenPublicUrlRequest(s3Key=s3Key)
            grpcResponse = self.stub.genPublicUrl(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return grpcResponse.publicUrl, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED 