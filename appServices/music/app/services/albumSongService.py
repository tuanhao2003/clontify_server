from app.repositories.albumSongRepo import AlbumSongRepo
from app.entities.albumSong import AlbumSong
from common.errorCodes import ErrorCodes
import uuid
from app.repositories.songsRepo import SongsRepo
from app.repositories.albumsRepo import AlbumsRepo

class AlbumSongService:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = AlbumSongRepo.filterAllPaginated(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            result = AlbumSongRepo.filterAll()
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
            if not albumId or not songId:
                return None, ErrorCodes.INVALID_INPUT
            albumId = uuid.UUID(albumId)
            songId = uuid.UUID(songId)
            song = SongsRepo.getById(songId)
            if not song:
                return None, ErrorCodes.NOT_FOUND
            album = AlbumsRepo.getById(albumId)
            if not album:
                return None, ErrorCodes.NOT_FOUND
            
            existing = AlbumSongRepo.getExactly(albumId, songId)
            if existing:
                return None, ErrorCodes.ALREADY_EXISTS
            albumSong = AlbumSong(albumId=albumId, songId=songId)
            result = AlbumSongRepo.create(albumSong)
            if not result:
                return None, ErrorCodes.CREATE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def doAddSongsToAlbum(albumId: str, songIds: list[str]):
        try:
            if not albumId or not songIds:
                return None, ErrorCodes.INVALID_INPUT
            albumId = uuid.UUID(albumId)
            songIds = [uuid.UUID(songId) for songId in songIds]
            songs = SongsRepo.getByIds(songIds)
            if not songs:
                return None, ErrorCodes.NOT_FOUND
            album = AlbumsRepo.getById(albumId)
            if not album:
                return None, ErrorCodes.NOT_FOUND
            
            addedSongs = []
            for song in songs:
                existing = AlbumSongRepo.getExactly(albumId, song.id)
                if not existing:
                    albumSong = AlbumSong(albumId=albumId, songId=song.id)
                    result = AlbumSongRepo.create(albumSong)
                    if not result:
                        return None, ErrorCodes.CREATE_FAILED
                    addedSongs.append(result)
            return addedSongs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDelete(albumId: str, songId: str):
        try:
            albumId = uuid.UUID(albumId)
            songId = uuid.UUID(songId)
            albumSong = AlbumSongRepo.getExactly(albumId, songId)
            if not albumSong:
                return None, ErrorCodes.NOT_FOUND
            result = AlbumSongRepo.delete(albumSong)
            if not result:
                return None, ErrorCodes.DELETE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def doHardDelete(albumId: str, songId: str):
        try:
            albumId = uuid.UUID(albumId)
            songId = uuid.UUID(songId)
            albumSong = AlbumSongRepo.getExactly(albumId, songId)
            if not albumSong:
                return None, ErrorCodes.NOT_FOUND
            result = AlbumSongRepo.hardDelete(albumSong)
            if not result:
                return None, ErrorCodes.DELETE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    