from app.repositories.albumSongRepo import AlbumSongRepo
from app.entities.albumSong import AlbumSong
from common.errorCodes import ErrorCodes

class AlbumSongService:
    @staticmethod
    def findById(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        albumSong = AlbumSongRepo.getById(id)
        if not albumSong:
            return None, ErrorCodes.NOT_FOUND
        return albumSong, None

    @staticmethod
    def findByAlbumId(albumId):
        if not albumId:
            return None, ErrorCodes.INVALID_INPUT
        albumSongs = AlbumSongRepo.filterByAlbumId(albumId)
        if not albumSongs:
            return None, ErrorCodes.NOT_FOUND
        return albumSongs, None

    @staticmethod
    def findBySongId(songId):
        if not songId:
            return None, ErrorCodes.INVALID_INPUT
        albumSongs = AlbumSongRepo.filterBySongId(songId)
        if not albumSongs:
            return None, ErrorCodes.NOT_FOUND
        return albumSongs, None

    @staticmethod
    def doCreate(albumId, songId, order=None):
        if not albumId or not songId:
            return None, ErrorCodes.INVALID_INPUT
        existing = AlbumSongRepo.filterByAlbumId(albumId)
        if existing and existing.filter(songId=songId).exists():
            return None, ErrorCodes.ALREADY_EXISTS
        albumSong = AlbumSong(
            albumId=albumId,
            songId=songId,
            order=order
        )
        created = AlbumSongRepo.create(albumSong)
        if not created:
            return None, ErrorCodes.CREATE_FAILED
        return created, None

    @staticmethod
    def doUpdate(albumSong: AlbumSong):
        if not albumSong.id:
            return None, ErrorCodes.INVALID_INPUT
        updated = AlbumSongRepo.update(albumSong)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        deleted = AlbumSongRepo.delete(id)
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None 