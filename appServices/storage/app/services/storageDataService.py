import uuid
import boto3
from django.conf import settings
from app.entities.storageData import StorageData
from app.repositories.storageDataRepo import StorageDataRepo
from common.errorCodes import ErrorCodes
from app.enums.fileTypeEnums import FileTypeEnums
from botocore.exceptions import ClientError
from app.grpc.grpcClients.usersGrpcClient import UsersGrpcClient


class StorageDataService:
    @staticmethod
    def uploadToS3(file: bytes, fileName: str, fileType: str):
        try:
            s3Client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            if not file or not fileName or not fileType or fileName == "" or fileType == "" or fileType not in FileTypeEnums.__members__:
                return None, ErrorCodes.INVALID_INPUT
            
            fileExtension = fileName.split('.')[-1]
            s3Key = f"{uuid.uuid4()}.{fileExtension}"
            
            s3Client.upload_fileobj(
                file,
                settings.AWS_STORAGE_BUCKET_NAME,
                s3Key,
                ExtraArgs={
                    'ACL': settings.AWS_DEFAULT_ACL,
                    'ContentType': fileType
                }
            )
            
            s3Url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3Key}"
            
            return {"key":s3Key, "url":s3Url}, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = StorageDataRepo.filterAllPaginated(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            result = StorageDataRepo.filterAll()
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findById(id: str):
        try:
            if not id:
                return None, ErrorCodes.INVALID_INPUT
            storageData = StorageDataRepo.getById(uuid.UUID(id))
            if not storageData:
                return None, ErrorCodes.NOT_FOUND
            return storageData, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByIds(ids: list[str]):
        try:
            if not ids:
                return None, ErrorCodes.INVALID_INPUT
            uuids = [uuid.UUID(id) for id in ids]
            storageData = StorageDataRepo.getByIds(uuids)
            if not storageData:
                return None, ErrorCodes.NOT_FOUND
            return storageData, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByFileNamePaginated(fileName: str, page: int = 1, pageSize: int = 10):
        try:
            if not fileName or fileName == "":
                return None, ErrorCodes.INVALID_INPUT
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = StorageDataRepo.filterByFileNamePaginated(fileName, page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByFileName(fileName: str):
        try:
            if not fileName or fileName == "":
                return None, ErrorCodes.INVALID_INPUT
            result = StorageDataRepo.filterByFileName(fileName)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByUserIdPaginated(userId: str, page: int = 1, pageSize: int = 10):
        try:
            if not userId or userId == "":
                return None, ErrorCodes.INVALID_INPUT
            
            userGrpcClient = UsersGrpcClient()
            _, error = userGrpcClient.findByID(userId)
            if error:
                return None, error
            
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = StorageDataRepo.filterByUserIdPaginated(uuid.UUID(userId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        finally:
            userGrpcClient.close()

    @staticmethod
    def findByUserId(userId: str):
        try:
            if not userId or userId == "":
                return None, ErrorCodes.INVALID_INPUT
            
            userGrpcClient = UsersGrpcClient()
            _, error = userGrpcClient.findByID(userId)
            if error:
                return None, error
            
            result = StorageDataRepo.filterByUserId(uuid.UUID(userId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByFileTypePaginated(fileType: str, page: int = 1, pageSize: int = 10):
        try:
            if not fileType or fileType == "" or fileType not in FileTypeEnums.__members__:
                return None, ErrorCodes.INVALID_INPUT
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = StorageDataRepo.filterByFileTypePaginated(FileTypeEnums[fileType], page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByFileType(fileType: str):
        try:
            if not fileType or fileType == "" or fileType not in FileTypeEnums.__members__:
                return None, ErrorCodes.INVALID_INPUT
            result = StorageDataRepo.filterByFileType(FileTypeEnums[fileType])
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doCreate(fileName: str, fileType: str, userId: str, fileUrl: str, description: str = None, fileSize: int = None):
        try:
            if not fileName or not fileType or not userId or fileName == "" or fileType == "" or userId == "":
                return None, ErrorCodes.INVALID_INPUT

            storageData = StorageData(
                fileName=fileName,
                fileType=fileType,
                userId=uuid.UUID(userId),
                fileUrl=fileUrl,
                fileSize=fileSize,
                description=description
            )
            created = StorageDataRepo.create(storageData)
            if not created:
                return None, ErrorCodes.CREATE_FAILED
            return created, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doUpdate(id: str, fileName: str = None, fileType: str = None, fileSize: int = None, fileUrl: str = None, description: str = None):
        try:
            if not id or id == "":
                return None, ErrorCodes.INVALID_INPUT

            currentStorageData = StorageDataRepo.getById(uuid.UUID(id))
            if not currentStorageData:
                return None, ErrorCodes.NOT_FOUND

            if fileName is not None:
                currentStorageData.fileName = fileName
            if fileType is not None:
                currentStorageData.fileType = fileType
            if fileSize is not None:
                currentStorageData.fileSize = fileSize
            if fileUrl is not None:
                currentStorageData.fileUrl = fileUrl
            if description is not None:
                currentStorageData.description = description

            updated = StorageDataRepo.update(currentStorageData)
            if not updated:
                return None, ErrorCodes.UPDATE_FAILED
            return updated, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDelete(id: str):
        try:
            if not id or id == "":
                return None, ErrorCodes.INVALID_INPUT

            currentStorageData = StorageDataRepo.getById(uuid.UUID(id))
            if not currentStorageData:
                return None, ErrorCodes.NOT_FOUND

            deleted = StorageDataRepo.delete(currentStorageData)
            if not deleted:
                return None, ErrorCodes.DELETE_FAILED
            return deleted, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED 