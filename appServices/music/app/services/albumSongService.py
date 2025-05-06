from app.repositories.albumSongRepo import AlbumSongRepo
from app.entities.albumSong import AlbumSong
from common.errorCodes import ErrorCodes
import uuid

class AlbumSongService:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = AlbumSongRepo.getAllPaginated(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            result = AlbumSongRepo.getAll()
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findExactly(albumId: str, songId: str):
        try:
            result = AlbumSongRepo.getExactly(uuid.UUID(albumId), uuid.UUID(songId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findByAlbumIdPaginated(albumId: str, page: int = 1, pageSize: int = 10):
        try:
            result = AlbumSongRepo.filterByAlbumIdPaginated(uuid.UUID(albumId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByAlbumId(albumId: str):
        try:
            result = AlbumSongRepo.filterByAlbumId(uuid.UUID(albumId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findBySongIdPaginated(songId: str, page: int = 1, pageSize: int = 10):
        try:
            result = AlbumSongRepo.filterBySongIdPaginated(uuid.UUID(songId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findBySongId(songId: str):
        try:
            result = AlbumSongRepo.filterBySongId(uuid.UUID(songId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def doCreate(albumId: str, songId: str):
        try:
            albumId = uuid.UUID(albumId)
            songId = uuid.UUID(songId)
            albumSong = AlbumSong(albumId=albumId, songId=songId)
            result = AlbumSongRepo.create(albumSong)
            if not result:
                return None, ErrorCodes.CREATE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDelete(albumId: str, songId: str):
        try:
            albumId = uuid.UUID(albumId)
            songId = uuid.UUID(songId)
            albumSong = AlbumSongRepo.getExactly(albumId, songId)
            result = AlbumSongRepo.delete(albumSong)
            if not result:
                return None, ErrorCodes.DELETE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    