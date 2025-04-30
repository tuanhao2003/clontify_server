from django.utils.timezone import now
from app.entities.albumSong import AlbumSong

class AlbumSongRepo:
    @staticmethod
    def getById(id):
        try:
            return AlbumSong.objects.get(id=id, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterByAlbumId(albumId):
        try:
            return AlbumSong.objects.filter(albumId=albumId, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterBySongId(songId):
        try:
            return AlbumSong.objects.filter(songId=songId, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def create(albumSong: AlbumSong):
        try:
            return AlbumSong.objects.create(
                id=albumSong.id,
                albumId=albumSong.albumId,
                songId=albumSong.songId,
                order=albumSong.order,
                isActive=albumSong.isActive
            )
        except Exception:
            return None

    @staticmethod
    def update(albumSong: AlbumSong):
        try:
            a = AlbumSong.objects.get(id=albumSong.id)
            a.albumId = albumSong.albumId
            a.songId = albumSong.songId
            a.order = albumSong.order
            a.isActive = albumSong.isActive
            a.updatedAt = now()
            a.save()
            return a
        except Exception:
            return None

    @staticmethod
    def delete(id):
        try:
            albumSong = AlbumSong.objects.get(id=id, isActive=True, deletedAt=None)
            albumSong.isActive = False
            albumSong.deletedAt = now()
            albumSong.save()
            return albumSong
        except Exception:
            return None 