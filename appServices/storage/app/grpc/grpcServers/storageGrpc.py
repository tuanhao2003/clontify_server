import grpc
from concurrent import futures
import time
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import storageService_pb2, storageService_pb2_grpc
from app.services.storageDataService import StorageDataService
from common.errorCodes import ErrorCodes

class StorageGrpc(storageService_pb2_grpc.StorageServiceServicer):
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

    def uploadToS3(self, request, context):
        try:
            file = request.file
            fileName = request.fileName
            fileType = request.fileType

            if not file or fileName or fileType or fileName == "" or fileType == "":
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Dữ liệu không hợp lệ")
                return None
            
            result, error = StorageDataService.uploadToS3(file=file, fileName=fileName, fileType=fileType)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return storageService_pb2.UploadToS3Response(
                key=result["key"],
                url=result["url"]
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
                 
    def findAll(self, request, context):
        try:
            result, error = StorageDataService.findAll()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
            for data in result:
                yield storageService_pb2.StorageData(
                    id=data.id,
                    userId=data.userId,
                    fileName=data.fileName,
                    fileType=data.fileType,
                    fileSize=data.fileSize,
                    fileUrl=data.fileUrl,
                    description=data.description,
                    createdAt=self._parseTimestamp(data.createdAt),
                    updatedAt=self._parseTimestamp(data.updatedAt),
                    deletedAt=self._parseTimestamp(data.deletedAt),
                    isActive=data.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
        
    def findById(self, request, context):
        try:
            id = str(request.str)
            if not id or id == "":
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return None
            result, error = StorageDataService.findById(id)
            if error:
                if error == ErrorCodes.NOT_FOUND:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Không tìm thấy dữ liệu")
                else:
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details(str(error))
                return None
                
            return storageService_pb2.StorageData(
                id=str(result.id),
                userId=str(result.userId),
                fileName=result.fileName,
                fileType=result.fileType,
                fileSize=str(result.fileSize),
                fileUrl=result.fileUrl,
                description=result.description,
                createdAt=self._parseTimestamp(result.createdAt),
                updatedAt=self._parseTimestamp(result.updatedAt),
                deletedAt=self._parseTimestamp(result.deletedAt),
                isActive=result.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Lỗi hệ thống: {str(e)}")
            return None
            
    def findByIds(self, request, context):
        try:
            ids = request.strs
            if not ids or len(ids) == 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return None
            result, error = StorageDataService.findByIds(ids)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for data in result:
                yield storageService_pb2.StorageData(
                    id=data.id,
                    userId=data.userId,
                    fileName=data.fileName,
                    fileType=data.fileType,
                    fileSize=data.fileSize,
                    fileUrl=data.fileUrl,
                    description=data.description,
                    createdAt=self._parseTimestamp(data.createdAt),
                    updatedAt=self._parseTimestamp(data.updatedAt),
                    deletedAt=self._parseTimestamp(data.deletedAt),
                    isActive=data.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findByFileType(self, request, context):
        try:
            fileType = request.str
            if not fileType or fileType == "":
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("File type không hợp lệ")
                return None
            result, error = StorageDataService.findByFileType(fileType)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for data in result:
                yield storageService_pb2.StorageData(
                    id=data.id,
                    userId=data.userId,
                    fileName=data.fileName,
                    fileType=data.fileType,
                    fileSize=data.fileSize,
                    fileUrl=data.fileUrl,
                    description=data.description,
                    createdAt=self._parseTimestamp(data.createdAt),
                    updatedAt=self._parseTimestamp(data.updatedAt),
                    deletedAt=self._parseTimestamp(data.deletedAt),
                    isActive=data.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
        
    def findByUserId(self, request, context):
        try:
            userId = request.str
            if not userId or userId == "":
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("User ID không hợp lệ")
                return None
            result, error = StorageDataService.findByUserId(userId)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for data in result:
                yield storageService_pb2.StorageData(
                    id=data.id,
                    userId=data.userId,
                    fileName=data.fileName,
                    fileType=data.fileType,
                    fileSize=data.fileSize,
                    fileUrl=data.fileUrl,
                    description=data.description,
                    createdAt=self._parseTimestamp(data.createdAt),
                    updatedAt=self._parseTimestamp(data.updatedAt),
                    deletedAt=self._parseTimestamp(data.deletedAt),
                    isActive=data.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
        
    def findByFileName(self, request, context):
        try:
            fileName = request.str
            if not fileName or fileName == "":
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("File name không hợp lệ")
                return None
            result, error = StorageDataService.findByFileName(fileName)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for data in result:
                yield storageService_pb2.StorageData(
                    id=data.id,
                    userId=data.userId,
                    fileName=data.fileName,
                    fileType=data.fileType,
                    fileSize=data.fileSize,
                    fileUrl=data.fileUrl,
                    description=data.description,
                    createdAt=self._parseTimestamp(data.createdAt),
                    updatedAt=self._parseTimestamp(data.updatedAt),
                    deletedAt=self._parseTimestamp(data.deletedAt),
                    isActive=data.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
        
    def doCreate(self, request, context):
        try:
            userId = request.userId
            fileName = request.fileName
            fileType = request.fileType
            fileSize = request.fileSize
            fileUrl = request.fileUrl
            description = request.description
            if not userId or not fileName or not fileType  or not fileUrl or userId == "" or fileName == "" or fileType == "" or fileUrl == "":
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Dữ liệu không hợp lệ")
                return None
            result, error = StorageDataService.doCreate(fileName=fileName, fileType=fileType, userId=userId, fileUrl=fileUrl, description=description, fileSize=fileSize)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return storageService_pb2.StorageData(
                id=result.id,
                userId=result.userId,
                fileName=result.fileName,
                fileType=result.fileType,
                fileSize=result.fileSize,
                fileUrl=result.fileUrl,
                description=result.description,
                createdAt=self._parseTimestamp(result.createdAt),
                updatedAt=self._parseTimestamp(result.updatedAt),
                deletedAt=self._parseTimestamp(result.deletedAt),
                isActive=result.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
        
    def doUpdate(self, request, context):
        try:
            id = request.id
            fileName = request.fileName
            fileType = request.fileType
            fileSize = request.fileSize
            fileUrl = request.fileUrl
            description = request.description
            if not id or id == "":
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return None
            result, error = StorageDataService.doUpdate(id=id, fileName=fileName, fileType=fileType, fileSize=fileSize, fileUrl=fileUrl, description=description)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return storageService_pb2.StorageData(
                id=result.id,
                userId=result.userId,
                fileName=result.fileName,
                fileType=result.fileType,
                fileSize=result.fileSize,
                fileUrl=result.fileUrl,
                description=result.description,
                createdAt=self._parseTimestamp(result.createdAt),
                updatedAt=self._parseTimestamp(result.updatedAt),
                deletedAt=self._parseTimestamp(result.deletedAt),
                isActive=result.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
        
    def doDelete(self, request, context):
        try:
            id = request.str
            if not id or id == "":
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return None
            result, error = StorageDataService.doDelete(id=id)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return storageService_pb2.StorageData(
                id=result.id,
                userId=result.userId,
                fileName=result.fileName,
                fileType=result.fileType,
                fileSize=result.fileSize,
                fileUrl=result.fileUrl,
                description=result.description,
                createdAt=self._parseTimestamp(result.createdAt),
                updatedAt=self._parseTimestamp(result.updatedAt),
                deletedAt=self._parseTimestamp(result.deletedAt),
                isActive=result.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def genPublicUrl(self, request, context):
        try:
            s3Key = request.s3Key
            if not s3Key or s3Key == "":
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("dữ liệu không hợp lệ")
                return None
            url, error = StorageDataService.genPublicUrl(s3Key)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Không tạo được public url")
                return None
            return storageService_pb2.GenPublicUrlResponse(publicUrl=url)
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