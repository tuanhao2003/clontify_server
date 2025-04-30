from app.repositories.albumsRepo import AlbumsRepo
from app.entities.albums import Albums
from common.errorCodes import ErrorCodes

class AlbumsService:
    @staticmethod
    def findById(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        album = AlbumsRepo.getById(id)
        if not album:
            return None, ErrorCodes.NOT_FOUND
        return album, None

    @staticmethod
    def findByName(name):
        if not name:
            return None, ErrorCodes.INVALID_INPUT
        albums = AlbumsRepo.getByName(name)
        if not albums:
            return None, ErrorCodes.NOT_FOUND
        return albums, None

    @staticmethod
    def doCreate(name, description=None, backgroundImage=None):
        if not name:
            return None, ErrorCodes.INVALID_INPUT
        existing = AlbumsRepo.getByName(name)
        if existing and existing.exists():
            return None, ErrorCodes.ALREADY_EXISTS
        album = Albums(
            name=name,
            description=description,
            backgroundImage=backgroundImage
        )
        created = AlbumsRepo.create(album)
        if not created:
            return None, ErrorCodes.CREATE_FAILED
        return created, None

    @staticmethod
    def doUpdate(album: Albums):
        if not album.id:
            return None, ErrorCodes.INVALID_INPUT
        updated = AlbumsRepo.update(album)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        deleted = AlbumsRepo.delete(id)
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None 