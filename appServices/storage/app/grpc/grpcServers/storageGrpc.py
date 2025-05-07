import grpc
from concurrent import futures
import time
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import storageService_pb2, storageService_pb2_grpc
from app.services.storageDataService import StorageDataService
from common.errorCodes import ErrorCodes

class StorageGrpc(storageService_pb2_grpc.StorageServiceServicer):
    def _parseTimestamp(self, timestamp):
        if isinstance(timestamp, datetime):
            return Timestamp(seconds=int(timestamp.replace(tzinfo=None).timestamp()), nanos=timestamp.microsecond * 1000)
        elif isinstance(timestamp, (int, float)):
            return Timestamp(seconds=int(timestamp), nanos=0)
        else:
            raise ValueError("Invalid timestamp format")

    def findAll(self, request, context):
        try:
            result, error = StorageDataService.findAll()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for item in result:
                yield storageService_pb2.StorageData(
                    id=str(item.id),
                    fileName=item.fileName,
                    fileType=item.fileType,
                    userId=str(item.userId),
                    fileSize=item.fileSize,
                    filePath=item.filePath,
                    fileUrl=item.fileUrl,
                    isActive=item.isActive,
                    createdAt=self._parseTimestamp(item.createdAt),
                    updatedAt=self._parseTimestamp(item.updatedAt),
                    deletedAt=self._parseTimestamp(item.deletedAt)
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findById(self, request, context):
        try:
            result, error = StorageDataService.findById(request.id)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return storageService_pb2.StorageData(
                id=str(result.id),
                fileName=result.fileName,
                fileType=result.fileType,
                userId=str(result.userId),
                fileSize=result.fileSize,
                filePath=result.filePath,
                fileUrl=result.fileUrl,
                isActive=result.isActive,
                createdAt=self._parseTimestamp(result.createdAt),
                updatedAt=self._parseTimestamp(result.updatedAt),
                deletedAt=self._parseTimestamp(result.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findByIds(self, request, context):
        try:
            result, error = StorageDataService.findByIds(request.ids)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for item in result:
                yield storageService_pb2.StorageData(
                    id=str(item.id),
                    fileName=item.fileName,
                    fileType=item.fileType,
                    userId=str(item.userId),
                    fileSize=item.fileSize,
                    filePath=item.filePath,
                    fileUrl=item.fileUrl,
                    isActive=item.isActive,
                    createdAt=self._parseTimestamp(item.createdAt),
                    updatedAt=self._parseTimestamp(item.updatedAt),
                    deletedAt=self._parseTimestamp(item.deletedAt)
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findByFileName(self, request, context):
        try:
            result, error = StorageDataService.findByFileName(request.fileName)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for item in result:
                yield storageService_pb2.StorageData(
                    id=str(item.id),
                    fileName=item.fileName,
                    fileType=item.fileType,
                    userId=str(item.userId),
                    fileSize=item.fileSize,
                    filePath=item.filePath,
                    fileUrl=item.fileUrl,
                    isActive=item.isActive,
                    createdAt=self._parseTimestamp(item.createdAt),
                    updatedAt=self._parseTimestamp(item.updatedAt),
                    deletedAt=self._parseTimestamp(item.deletedAt)
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findByUserId(self, request, context):
        try:
            result, error = StorageDataService.findByUserId(request.userId)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for item in result:
                yield storageService_pb2.StorageData(
                    id=str(item.id),
                    fileName=item.fileName,
                    fileType=item.fileType,
                    userId=str(item.userId),
                    fileSize=item.fileSize,
                    filePath=item.filePath,
                    fileUrl=item.fileUrl,
                    isActive=item.isActive,
                    createdAt=self._parseTimestamp(item.createdAt),
                    updatedAt=self._parseTimestamp(item.updatedAt),
                    deletedAt=self._parseTimestamp(item.deletedAt)
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findByFileType(self, request, context):
        try:
            result, error = StorageDataService.findByFileType(request.fileType)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for item in result:
                yield storageService_pb2.StorageData(
                    id=str(item.id),
                    fileName=item.fileName,
                    fileType=item.fileType,
                    userId=str(item.userId),
                    fileSize=item.fileSize,
                    filePath=item.filePath,
                    fileUrl=item.fileUrl,
                    isActive=item.isActive,
                    createdAt=self._parseTimestamp(item.createdAt),
                    updatedAt=self._parseTimestamp(item.updatedAt),
                    deletedAt=self._parseTimestamp(item.deletedAt)
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def create(self, request, context):
        try:
            result, error = StorageDataService.doCreate(
                request.fileName,
                request.fileType,
                request.userId,
                request.fileSize,
                request.filePath,
                request.fileUrl
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return storageService_pb2.StorageData(
                id=str(result.id),
                fileName=result.fileName,
                fileType=result.fileType,
                userId=str(result.userId),
                fileSize=result.fileSize,
                filePath=result.filePath,
                fileUrl=result.fileUrl,
                isActive=result.isActive,
                createdAt=self._parseTimestamp(result.createdAt),
                updatedAt=self._parseTimestamp(result.updatedAt),
                deletedAt=self._parseTimestamp(result.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def update(self, request, context):
        try:
            result, error = StorageDataService.doUpdate(
                request.id,
                request.fileName,
                request.fileType,
                request.fileSize,
                request.filePath,
                request.fileUrl
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return storageService_pb2.StorageData(
                id=str(result.id),
                fileName=result.fileName,
                fileType=result.fileType,
                userId=str(result.userId),
                fileSize=result.fileSize,
                filePath=result.filePath,
                fileUrl=result.fileUrl,
                isActive=result.isActive,
                createdAt=self._parseTimestamp(result.createdAt),
                updatedAt=self._parseTimestamp(result.updatedAt),
                deletedAt=self._parseTimestamp(result.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def delete(self, request, context):
        try:
            result, error = StorageDataService.doDelete(request.id)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return storageService_pb2.StorageData(
                id=str(result.id),
                fileName=result.fileName,
                fileType=result.fileType,
                userId=str(result.userId),
                fileSize=result.fileSize,
                filePath=result.filePath,
                fileUrl=result.fileUrl,
                isActive=result.isActive,
                createdAt=self._parseTimestamp(result.createdAt),
                updatedAt=self._parseTimestamp(result.updatedAt),
                deletedAt=self._parseTimestamp(result.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storageService_pb2_grpc.add_StorageServiceServicer_to_server(StorageGrpc(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)