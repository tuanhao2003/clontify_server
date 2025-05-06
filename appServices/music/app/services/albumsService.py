from app.repositories.albumsRepo import AlbumsRepo
from app.entities.albums import Albums
from common.errorCodes import ErrorCodes
from app.services.albumSongService import AlbumSongService
import uuid
class AlbumsService:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = AlbumsRepo.findAllPaginated(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            result = AlbumsRepo.findAll()
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
            album = AlbumsRepo.getById(uuid.UUID(id))
            if not album:
                return None, ErrorCodes.NOT_FOUND
            return album, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByIds(ids: list[str]):
        try:
            if not ids:
                return None, ErrorCodes.INVALID_INPUT
            uuids = [uuid.UUID(id) for id in ids]
            albums = AlbumsRepo.getByIds(uuids)
            if not albums:
                return None, ErrorCodes.NOT_FOUND
            return albums, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByNamePaginated(name: str, page: int = 1, pageSize: int = 10):
        try:
            if not name:
                return None, ErrorCodes.INVALID_INPUT
            albums = AlbumsRepo.filterByNamePaginated(name, page, pageSize)
            if not albums:
                return None, ErrorCodes.NOT_FOUND
            return albums, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByName(name: str):
        try:
            if not name:
                return None, ErrorCodes.INVALID_INPUT
            albums = AlbumsRepo.filterByName(name)
            if not albums:
                return None, ErrorCodes.NOT_FOUND
            return albums, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    @staticmethod
    def findBySongId(songId: str):
        try:
            if not songId:
                return None, ErrorCodes.INVALID_INPUT
            albumsIds = AlbumSongService.findBySongId(songId)
            if not albumsIds:
                return None, ErrorCodes.NOT_FOUND
            albums = AlbumsRepo.findByIds(albumsIds)
            if not albums:
                return None, ErrorCodes.NOT_FOUND
            return albums, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doCreate(name, description=None, backgroundImage=None):
        try:
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
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doUpdate(id, name=None, description=None, backgroundImage=None):
        try:
            if not id:
                return None, ErrorCodes.INVALID_INPUT
            currentAlbum = AlbumsRepo.getById(id)
            if not currentAlbum:
                return None, ErrorCodes.NOT_FOUND
            if name is not None:
                currentAlbum.name = name
            if description is not None:
                currentAlbum.description = description
            if backgroundImage is not None:
                currentAlbum.backgroundImage = backgroundImage
            updated = AlbumsRepo.update(currentAlbum)
            if not updated:
                return None, ErrorCodes.UPDATE_FAILED
            return updated, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDelete(id):
        try:
            if not id:
                return None, ErrorCodes.INVALID_INPUT
            currentAlbum = AlbumsRepo.getById(id)
            if not currentAlbum:
                return None, ErrorCodes.NOT_FOUND
            deleted = AlbumsRepo.delete(currentAlbum)
            if not deleted:
                return None, ErrorCodes.DELETE_FAILED
            return deleted, None 
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

