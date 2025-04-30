from django.utils.timezone import now
from app.entities.playlistSong import PlaylistSong

class PlaylistSongRepo:
    @staticmethod
    def getById(id):
        try:
            return PlaylistSong.objects.get(id=id, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterByPlaylistId(playlistId):
        try:
            return PlaylistSong.objects.filter(playlistId=playlistId, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterBySongId(songId):
        try:
            return PlaylistSong.objects.filter(songId=songId, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def create(playlistSong: PlaylistSong):
        try:
            return PlaylistSong.objects.create(
                id=playlistSong.id,
                playlistId=playlistSong.playlistId,
                songId=playlistSong.songId,
                order=playlistSong.order,
                isActive=playlistSong.isActive
            )
        except Exception:
            return None

    @staticmethod
    def update(playlistSong: PlaylistSong):
        try:
            p = PlaylistSong.objects.get(id=playlistSong.id)
            p.playlistId = playlistSong.playlistId
            p.songId = playlistSong.songId
            p.order = playlistSong.order
            p.isActive = playlistSong.isActive
            p.updatedAt = now()
            p.save()
            return p
        except Exception:
            return None

    @staticmethod
    def delete(id):
        try:
            playlistSong = PlaylistSong.objects.get(id=id, isActive=True, deletedAt=None)
            playlistSong.isActive = False
            playlistSong.deletedAt = now()
            playlistSong.save()
            return playlistSong
        except Exception:
            return None 