from app.repositories.playlistSongRepo import PlaylistSongRepo
from app.entities.playlistSong import PlaylistSong
from common.errorCodes import ErrorCodes

class PlaylistSongService:
    @staticmethod
    def findById(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        playlistSong = PlaylistSongRepo.getById(id)
        if not playlistSong:
            return None, ErrorCodes.NOT_FOUND
        return playlistSong, None

    @staticmethod
    def findByPlaylistId(playlistId):
        if not playlistId:
            return None, ErrorCodes.INVALID_INPUT
        playlistSongs = PlaylistSongRepo.filterByPlaylistId(playlistId)
        if not playlistSongs:
            return None, ErrorCodes.NOT_FOUND
        return playlistSongs, None

    @staticmethod
    def findBySongId(songId):
        if not songId:
            return None, ErrorCodes.INVALID_INPUT
        playlistSongs = PlaylistSongRepo.filterBySongId(songId)
        if not playlistSongs:
            return None, ErrorCodes.NOT_FOUND
        return playlistSongs, None

    @staticmethod
    def doCreate(playlistId, songId, order=None):
        if not playlistId or not songId:
            return None, ErrorCodes.INVALID_INPUT
        # Kiểm tra trùng (playlistId, songId)
        existing = PlaylistSongRepo.filterByPlaylistId(playlistId)
        if existing and existing.filter(songId=songId).exists():
            return None, ErrorCodes.ALREADY_EXISTS
        playlistSong = PlaylistSong(
            playlistId=playlistId,
            songId=songId,
            order=order
        )
        created = PlaylistSongRepo.create(playlistSong)
        if not created:
            return None, ErrorCodes.CREATE_FAILED
        return created, None

    @staticmethod
    def doUpdate(playlistSong: PlaylistSong):
        if not playlistSong.id:
            return None, ErrorCodes.INVALID_INPUT
        updated = PlaylistSongRepo.update(playlistSong)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        deleted = PlaylistSongRepo.delete(id)
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None 