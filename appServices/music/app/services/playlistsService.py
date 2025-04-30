from app.repositories.playlistsRepo import PlaylistsRepo
from app.entities.playlists import Playlists
from common.errorCodes import ErrorCodes

class PlaylistsService:
    @staticmethod
    def findById(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        playlist = PlaylistsRepo.getById(id)
        if not playlist:
            return None, ErrorCodes.NOT_FOUND
        return playlist, None

    @staticmethod
    def findByName(name):
        if not name:
            return None, ErrorCodes.INVALID_INPUT
        playlists = PlaylistsRepo.getByName(name)
        if not playlists:
            return None, ErrorCodes.NOT_FOUND
        return playlists, None

    @staticmethod
    def findByOwnerId(ownerId):
        if not ownerId:
            return None, ErrorCodes.INVALID_INPUT
        playlists = PlaylistsRepo.filterByOwnerId(ownerId)
        if not playlists:
            return None, ErrorCodes.NOT_FOUND
        return playlists, None

    @staticmethod
    def doCreate(name, ownerId, description=None):
        if not name or not ownerId:
            return None, ErrorCodes.INVALID_INPUT
        existing = PlaylistsRepo.getByName(name)
        if existing and existing.filter(ownerId=ownerId).exists():
            return None, ErrorCodes.ALREADY_EXISTS
        playlist = Playlists(
            name=name,
            ownerId=ownerId,
            description=description
        )
        created = PlaylistsRepo.create(playlist)
        if not created:
            return None, ErrorCodes.CREATE_FAILED
        return created, None

    @staticmethod
    def doUpdate(playlist: Playlists):
        if not playlist.id:
            return None, ErrorCodes.INVALID_INPUT
        updated = PlaylistsRepo.update(playlist)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        deleted = PlaylistsRepo.delete(id)
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None 