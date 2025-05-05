from app.repositories.genresRepo import GenresRepo
from app.entities.genres import Genres
from common.errorCodes import ErrorCodes
import uuid
from app.services.genreSongService import GenreSongService

class GenresService:
    @staticmethod
    def findAll(page: int = 1, pageSize: int = 10):
        try:
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = GenresRepo.findAll(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    @staticmethod
    def findById(id: str):
        try:
            if not id:
                return None, ErrorCodes.INVALID_INPUT
            genre = GenresRepo.getById(uuid.UUID(id))
            if not genre:
                return None, ErrorCodes.NOT_FOUND
            return genre, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByName(name: str, page: int = 1, pageSize: int = 10):
        try:
            if not name:
                return None, ErrorCodes.INVALID_INPUT
            genres = GenresRepo.getByName(name, page, pageSize)
            if not genres:
                return None, ErrorCodes.NOT_FOUND
            return genres, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    @staticmethod
    def findBySongId(songId: str):
        try:
            if not songId:
                return None, ErrorCodes.INVALID_INPUT
            genreIds = GenreSongService.getBySongId(songId)
            if not genreIds:
                return None, ErrorCodes.NOT_FOUND
            genres = GenresRepo.getByIds(genreIds)
            if not genres:
                return None, ErrorCodes.NOT_FOUND
            return genres, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    @staticmethod
    def doCreate(name: str, description: str = None):
        try:
            if not name:
                return None, ErrorCodes.INVALID_INPUT
            existing = GenresRepo.getByName(name)
            if existing and existing.exists():
                return None, ErrorCodes.ALREADY_EXISTS
            genre = Genres(
                name=name,
                description=description
            )
            created = GenresRepo.create(genre)
            if not created:
                return None, ErrorCodes.CREATE_FAILED
            return created, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doUpdate(id: str, name: str, description: str = None):
        try:
            if not id or not name or name == "":
                return None, ErrorCodes.INVALID_INPUT
            currentGenre = GenresRepo.getById(uuid.UUID(id))
            if not currentGenre:
                return None, ErrorCodes.NOT_FOUND
            if name is not None:
                currentGenre.name = name
            if description is not None:
                currentGenre.description = description
            updated = GenresRepo.update(currentGenre)
            if not updated:
                return None, ErrorCodes.UPDATE_FAILED
            return updated, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDelete(id: str):
        try:
            if not id:
                return None, ErrorCodes.INVALID_INPUT
            currentGenre = GenresRepo.getById(uuid.UUID(id))
            if not currentGenre:
                return None, ErrorCodes.NOT_FOUND
            deleted = GenresRepo.delete(currentGenre)
            if not deleted:
                return None, ErrorCodes.DELETE_FAILED
            return deleted, None 
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
