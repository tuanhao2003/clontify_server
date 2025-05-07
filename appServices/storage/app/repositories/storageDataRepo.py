from django.utils.timezone import now
from app.entities.storageData import StorageData
from django.core.paginator import Paginator
from django.db import models
import uuid

class StorageDataRepo:
    @staticmethod
    def filterAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = StorageData.objects.filter(isActive=True)
            paginator = Paginator(result, pageSize)
            return {
                'result': paginator.get_page(page),
                'total': paginator.count,
                'totalPages': paginator.num_pages,
                'currentPage': page
            }
        except Exception:
            return None

    @staticmethod
    def filterAll():
        try:
            return StorageData.objects.filter(isActive=True)
        except Exception:
            return None

    @staticmethod
    def getById(id: uuid.UUID):
        try:
            return StorageData.objects.get(id=id, isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def getByIds(ids: list[uuid.UUID]):
        try:
            return StorageData.objects.filter(id__in=ids, isActive=True)
        except Exception:
            return None

    @staticmethod
    def filterByFileNamePaginated(fileName: str, page: int = 1, pageSize: int = 10):
        try:
            result = StorageData.objects.filter(fileName__icontains=fileName, isActive=True)
            paginator = Paginator(result, pageSize)
            return {
                'result': paginator.get_page(page),
                'total': paginator.count,
                'totalPages': paginator.num_pages,
                'currentPage': page
            }
        except Exception:
            return None

    @staticmethod
    def filterByFileName(fileName: str):
        try:
            return StorageData.objects.filter(fileName__icontains=fileName, isActive=True)
        except Exception:
            return None
        
    @staticmethod
    def filterByUserId(userId: uuid.UUID):
        try:
            return StorageData.objects.filter(userId=userId, isActive=True)
        except Exception:
            return None

    @staticmethod
    def filterByUserIdPaginated(userId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            result = StorageData.objects.filter(userId=userId, isActive=True)
            paginator = Paginator(result, pageSize)
            return {
                'result': paginator.get_page(page),
                'total': paginator.count,
                'totalPages': paginator.num_pages,
                'currentPage': page
            }
        except Exception:
            return None

    @staticmethod
    def filterByFileType(fileType: str):
        try:
            return StorageData.objects.filter(fileType=fileType, isActive=True)
        except Exception:
            return None

    @staticmethod
    def filterByFileTypePaginated(fileType: str, page: int = 1, pageSize: int = 10):
        try:
            result = StorageData.objects.filter(fileType=fileType, isActive=True)
            paginator = Paginator(result, pageSize)
            return {
                'result': paginator.get_page(page),
                'total': paginator.count,
                'totalPages': paginator.num_pages,
                'currentPage': page
            }
        except Exception:
            return None

    @staticmethod
    def create(storageData: StorageData):
        try:
            storageData.save()
            return storageData
        except Exception:
            return None

    @staticmethod
    def update(storageData: StorageData):
        try:
            storageData.updatedAt = now()
            storageData.save()
            return storageData
        except Exception:
            return None

    @staticmethod
    def delete(storageData: StorageData):
        try:
            storageData.isActive = False
            storageData.deletedAt = now()
            storageData.save()
            return storageData
        except Exception:
            return None 