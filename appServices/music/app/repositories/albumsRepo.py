from django.utils.timezone import now
from app.entities.albums import Albums
from django.core.paginator import Paginator
import uuid

class AlbumsRepo:
    @staticmethod
    def findAll(page: int = 1, pageSize: int = 10):
        try:
            result = Albums.objects.filter(isActive=True)
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
    def getById(id: uuid.UUID):
        try:
            return Albums.objects.get(id=id, isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def findByIds(ids: list[uuid.UUID]):
        try:
            return Albums.objects.filter(id__in=ids, isActive=True)
        except Exception:
            return None

    @staticmethod
    def filterByName(name: str, page: int = 1, pageSize: int = 10):
        try:
            result = Albums.objects.filter(name__icontains=name, isActive=True)
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
    def create(album: Albums):
        try:
            album.save()
            return album
        except Exception:
            return None

    @staticmethod
    def update(album: Albums):
        try:
            album.updatedAt = now()
            album.save()
            return album
        except Exception:
            return None

    @staticmethod
    def delete(album: Albums):
        try:
            album.isActive = False
            album.deletedAt = now()
            album.save()
            return album
        except Exception:
            return None 