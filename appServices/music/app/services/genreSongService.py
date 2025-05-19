from app.repositories.genreSongRepo import GenreSongRepo
from app.entities.genreSong import GenreSong
from common.errorCodes import ErrorCodes
from app.repositories.genresRepo import GenresRepo
from app.repositories.songsRepo import SongsRepo
import uuid

class GenreSongService:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = GenreSongRepo.filterAllPaginated(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            result = GenreSongRepo.filterAll()
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findExactly(genreId: str, songId: str):
        try:
            result = GenreSongRepo.getExactly(uuid.UUID(genreId), uuid.UUID(songId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findByGenreIdPaginated(genreId: str, page: int = 1, pageSize: int = 10):
        try:
            result = GenreSongRepo.filterByGenreIdPaginated(uuid.UUID(genreId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByGenreId(genreId: str):
        try:
            result = GenreSongRepo.filterByGenreId(uuid.UUID(genreId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findBySongIdPaginated(songId: str, page: int = 1, pageSize: int = 10):
        try:
            result = GenreSongRepo.filterBySongIdPaginated(uuid.UUID(songId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findBySongId(songId: str):
        try:
            result = GenreSongRepo.filterBySongId(uuid.UUID(songId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def doCreate(genreId: str, songId: str):
        try:
            genreId = uuid.UUID(genreId)
            songId = uuid.UUID(songId)
            genre = GenresRepo.getById(genreId)
            if not genre:
                return None, ErrorCodes.NOT_FOUND
            song = SongsRepo.getById(songId)
            if not song:
                return None, ErrorCodes.NOT_FOUND
            if GenreSongRepo.getExactly(genreId, songId):
                return None, ErrorCodes.ALREADY_EXISTS
            
            genreSong = GenreSong(genreId=genreId, songId=songId)
            result = GenreSongRepo.create(genreSong)
            if not result:
                return None, ErrorCodes.CREATE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDelete(genreId: str, songId: str):
        try:
            genreId = uuid.UUID(genreId)
            songId = uuid.UUID(songId)
            genreSong = GenreSongRepo.getExactly(genreId, songId)
            if not genreSong:
                return None, ErrorCodes.NOT_FOUND
            result = GenreSongRepo.delete(genreSong)
            if not result:
                return None, ErrorCodes.DELETE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    @staticmethod
    def doHardDelete(genreId: str, songId: str):
        try:
            genreId = uuid.UUID(genreId)
            songId = uuid.UUID(songId)
            genreSong = GenreSongRepo.getExactly(genreId, songId)
            if not genreSong:
                return None, ErrorCodes.NOT_FOUND
            result = GenreSongRepo.hardDelete(genreSong)
            if not result:
                return None, ErrorCodes.DELETE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED