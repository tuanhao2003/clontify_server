from django.utils.timezone import now
from app.entities.favorites import Favorites
from django.core.paginator import Paginator
import uuid


class FavoritesRepo:
    @staticmethod
    def filterAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = Favorites.objects.filter(isActive=True)
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
            return Favorites.objects.filter(isActive=True)
        except Exception:
            return None

    @staticmethod
    def getExactly(profileId: uuid.UUID, songId: uuid.UUID):
        try:
            return Favorites.objects.get(profileID=profileId, songID=songId, isActive=True)
        except Exception:
            return None

    @staticmethod
    def filterByProfileId(profileId: uuid.UUID):
        try:
            return Favorites.objects.filter(profileID=profileId, isActive=True)
        except Exception:
            return None

    @staticmethod
    def filterByProfileIdPaginated(profileId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            result = Favorites.objects.filter(profileID=profileId, isActive=True)
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
    def filterBySongId(songId: uuid.UUID):
        try:
            return Favorites.objects.filter(songID=songId, isActive=True)
        except Exception:
            return None

    @staticmethod
    def filterBySongIdPaginated(songId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            result = Favorites.objects.filter(songID=songId, isActive=True)
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
    def create(favorite: Favorites):
        try:
            favorite.save()
            return favorite
        except Exception:
            return None

    @staticmethod
    def update(favorite: Favorites):
        try:
            favorite.updatedAt = now()
            favorite.save()
            return favorite
        except Exception:
            None

    @staticmethod
    def delete(favorite: Favorites):
        try:
            favorite.isActive = False
            favorite.deletedAt = now()
            favorite.save()
            return favorite
        except Exception:
            return None 