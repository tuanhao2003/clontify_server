from django.utils.timezone import now
from app.entities.albumSong import AlbumSong
from django.core.paginator import Paginator
import uuid

class AlbumSongRepo:
    @staticmethod
    def getAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = AlbumSong.objects.filter(isActive=True)
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
            return AlbumSong.objects.filter(isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def getExactly(albumId: uuid.UUID, songId: uuid.UUID):
        try:
            return AlbumSong.objects.get(albumId=albumId, songId=songId, isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def filterByAlbumIdPaginated(albumId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            result = AlbumSong.objects.filter(albumId=albumId, isActive=True)
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
    def filterByAlbumId(albumId: uuid.UUID):
        try:
            return AlbumSong.objects.filter(albumId=albumId, isActive=True)
        except Exception:
            return None
        
    @staticmethod
    def filterBySongIdPaginated(songId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            result = AlbumSong.objects.filter(songId=songId, isActive=True)
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
            return AlbumSong.objects.filter(songId=songId, isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def create(albumSong: AlbumSong):
        try:
            albumSong.save()
            return albumSong
        except Exception:
            return None

    @staticmethod
    def delete(albumSong: AlbumSong):
        try:
            albumSong.isActive = False
            albumSong.deletedAt = now()
            albumSong.save()
            return albumSong
        except Exception:
            return None