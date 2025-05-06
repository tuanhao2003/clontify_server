from django.utils.timezone import now
from app.entities.songSubArtist import SongSubArtist
from django.core.paginator import Paginator
import uuid

class SongSubArtistRepo:
    @staticmethod
    def getAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = SongSubArtist.objects.filter(isActive=True)
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
            return SongSubArtist.objects.filter(isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def getExactly(songId: uuid.UUID, artistId: uuid.UUID):
        try:
            return SongSubArtist.objects.get(songId=songId, artistId=artistId, isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def filterBySongIdPaginated(songId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            result = SongSubArtist.objects.filter(songId=songId, isActive=True)
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
            return SongSubArtist.objects.filter(songId=songId, isActive=True)
        except Exception:
            return None
        
    @staticmethod
    def filterByArtistIdPaginated(artistId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            result = SongSubArtist.objects.filter(artistId=artistId, isActive=True)
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
    def filterByArtistId(artistId: uuid.UUID):
        try:
            return SongSubArtist.objects.filter(artistId=artistId, isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def create(songSubArtist: SongSubArtist):
        try:
            songSubArtist.save()
            return songSubArtist
        except Exception:
            return None
        
    @staticmethod
    def delete(songSubArtist: SongSubArtist):
        try:
            songSubArtist.isActive = False
            songSubArtist.deletedAt = now()
            songSubArtist.save()
            return songSubArtist
        except Exception:
            return None 