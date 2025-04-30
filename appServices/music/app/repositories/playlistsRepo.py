from django.utils.timezone import now
from app.entities.playlists import Playlists

class PlaylistsRepo:
    @staticmethod
    def getById(id):
        try:
            return Playlists.objects.get(id=id, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterByName(name):
        try:
            return Playlists.objects.filter(name__icontains=name, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterByOwnerId(ownerId):
        try:
            return Playlists.objects.filter(ownerId=ownerId, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def create(playlist: Playlists):
        try:
            return Playlists.objects.create(
                id=playlist.id,
                name=playlist.name,
                description=playlist.description,
                ownerId=playlist.ownerId,
                isActive=playlist.isActive
            )
        except Exception:
            return None

    @staticmethod
    def update(playlist: Playlists):
        try:
            p = Playlists.objects.get(id=playlist.id)
            p.name = playlist.name
            p.description = playlist.description
            p.ownerId = playlist.ownerId
            p.isActive = playlist.isActive
            p.updatedAt = now()
            p.save()
            return p
        except Exception:
            return None

    @staticmethod
    def delete(id):
        try:
            playlist = Playlists.objects.get(id=id, isActive=True, deletedAt=None)
            playlist.isActive = False
            playlist.deletedAt = now()
            playlist.save()
            return playlist
        except Exception:
            return None 