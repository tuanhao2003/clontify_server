from django.utils.timezone import now
from app.entities.songs import Songs

class SongsRepo:
    @staticmethod
    def getById(id):
        try:
            return Songs.objects.get(id=id, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterByTitle(title):
        try:
            return Songs.objects.filter(title__icontains=title, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterByArtistId(artistId):
        try:
            return Songs.objects.filter(artistId=artistId, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterByGenreId(genreId):
        try:
            return Songs.objects.filter(genreId=genreId, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def create(id: str, title: str, description: str, artistId: str, audioUrl: str, backgroundImage: str, duration: int):
        try:
            return Songs.objects.create(
                id = id,
                title = title,
                description = description,
                artistId = artistId,
                audioUrl = audioUrl,
                backgroundImage = backgroundImage,
                duration = duration,
            )
        except Exception:
            return None

    @staticmethod
    def update(title: str, description: str, artistId: str, genreId: str, audioUrl: str, backgroundImage: str, duration: int):
        try:
            s = Songs.objects.get(id=song.id)
            s.title = song.title
            s.artistId = song.artistId
            s.genreId = song.genreId
            s.audioUrl = song.audioUrl
            s.backgroundImage = song.backgroundImage
            s.duration = song.duration
            s.isActive = song.isActive
            s.updatedAt = now()
            s.save()
            return s
        except Exception:
            return None

    @staticmethod
    def delete(id):
        try:
            song = Songs.objects.get(id=id, isActive=True, deletedAt=None)
            song.isActive = False
            song.deletedAt = now()
            song.save()
        except Exception:
            return None 