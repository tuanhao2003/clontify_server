from django.utils.timezone import now
from app.entities.genreSong import GenreSong
from django.core.paginator import Paginator
import uuid

class GenreSongRepo:
    @staticmethod
    def getAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = GenreSong.objects.filter(isActive=True)
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
    def getAll():
        try:
            return GenreSong.objects.filter(isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def getExactly(genreId: uuid.UUID, songId: uuid.UUID):
        try:
            return GenreSong.objects.get(genreId=genreId, songId=songId, isActive=True)
        except Exception:
            return None
        
    @staticmethod
    def filterByGenreIdPaginated(genreId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            result = GenreSong.objects.filter(genreId=genreId, isActive=True)
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
    def filterByGenreId(genreId: uuid.UUID):
        try:
            return GenreSong.objects.filter(genreId=genreId, isActive=True)
        except Exception:
            return None
        
    @staticmethod
    def filterBySongIdPaginated(songId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            result = GenreSong.objects.filter(songId=songId, isActive=True)
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
            return GenreSong.objects.filter(songId=songId, isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def create(genreSong: GenreSong):
        try:
            genreSong.save()
            return genreSong
        except Exception:
            return None

    @staticmethod
    def delete(genreSong: GenreSong):
        try:
            genreSong.isActive = False
            genreSong.deletedAt = now()
            genreSong.save()
            return genreSong
        except Exception:
            return None