from django.utils.timezone import now
from app.entities.genres import Genres
from django.core.paginator import Paginator
import uuid

class GenresRepo:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = Genres.objects.filter(isActive=True)
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
    def findAll():
        try:
            return Genres.objects.filter(isActive=True)
        except Exception:
            return None

    @staticmethod
    def getById(id: uuid.UUID):
        try:
            return Genres.objects.get(id=id, isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def getByIds(ids: list[uuid.UUID]):
        try:
            return Genres.objects.filter(id__in=ids, isActive=True)
        except Exception:
            return None

    @staticmethod
    def filterByNamePaginated(name: str, page: int = 1, pageSize: int = 10):
        try:
            result = Genres.objects.filter(name__icontains=name, isActive=True)
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
    def filterByName(name: str):
        try:
            return Genres.objects.filter(name__icontains=name, isActive=True)
        except Exception:
            return None

    @staticmethod
    def create(genre: Genres):
        try:
            genre.save()
            return genre
        except Exception:
            return None

    @staticmethod
    def update(genre: Genres):
        try:
            genre.updatedAt = now()
            genre.save()
            return genre
        except Exception:
            return None

    @staticmethod
    def delete(genre: Genres):
        try:
            genre.isActive = False
            genre.deletedAt = now()
            genre.save()
            return genre
        except Exception:
            return None 