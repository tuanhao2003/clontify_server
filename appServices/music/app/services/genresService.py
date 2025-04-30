from app.repositories.genresRepo import GenresRepo
from app.entities.genres import Genres
from common.errorCodes import ErrorCodes

class GenresService:
    @staticmethod
    def findById(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        genre = GenresRepo.getById(id)
        if not genre:
            return None, ErrorCodes.NOT_FOUND
        return genre, None

    @staticmethod
    def findByName(name):
        if not name:
            return None, ErrorCodes.INVALID_INPUT
        genres = GenresRepo.getByName(name)
        if not genres:
            return None, ErrorCodes.NOT_FOUND
        return genres, None

    @staticmethod
    def doCreate(name, description=None):
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

    @staticmethod
    def doUpdate(genre: Genres):
        if not genre.id:
            return None, ErrorCodes.INVALID_INPUT
        updated = GenresRepo.update(genre)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        deleted = GenresRepo.delete(id)
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None 