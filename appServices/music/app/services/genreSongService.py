from app.repositories.genreSongRepo import GenreSongRepo
from app.entities.genreSong import GenreSong
from common.errorCodes import ErrorCodes
import uuid

class GenreSongService:
    @staticmethod
    def findAll(page: int = 1, pageSize: int = 10):
        try:
            result = GenreSongRepo.getAll(page, pageSize)
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
    def findByGenreId(genreId: str, page: int = 1, pageSize: int = 10):
        try:
            result = GenreSongRepo.filterByGenreId(uuid.UUID(genreId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findBySongId(songId: str, page: int = 1, pageSize: int = 10):
        try:
            result = GenreSongRepo.filterBySongId(uuid.UUID(songId), page, pageSize)
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
            genreSong = GenreSong(genreId=genreId, songId=songId)
            result = GenreSongRepo.create(genreSong)
            if not result:
                return None, ErrorCodes.CREATE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def doUpdate(genreId: str, songId: str):
        try:
            genreId = uuid.UUID(genreId)
            songId = uuid.UUID(songId)
            genreSong =  GenreSong(genreId=genreId, songId=songId)
            result = GenreSongRepo.update(genreSong)
            if not result:
                return None, ErrorCodes.UPDATE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED


    @staticmethod
    def doDelete(genreId: str, songId: str):
        try:
            genreId = uuid.UUID(genreId)
            songId = uuid.UUID(songId)
            genreSong =  GenreSong(genreId=genreId, songId=songId)
            result = GenreSongRepo.delete(genreSong)
            if not result:
                return None, ErrorCodes.DELETE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    