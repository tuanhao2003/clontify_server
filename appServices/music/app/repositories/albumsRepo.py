from django.utils.timezone import now
from app.entities.albums import Albums

class AlbumsRepo:
    @staticmethod
    def getById(id):
        try:
            return Albums.objects.get(id=id, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterByName(name):
        try:
            return Albums.objects.filter(name__icontains=name, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def create(album: Albums):
        try:
            return Albums.objects.create(
                id=album.id,
                name=album.name,
                description=album.description,
                backgroundImage=album.backgroundImage,
                isActive=album.isActive
            )
        except Exception:
            return None

    @staticmethod
    def update(album: Albums):
        try:
            a = Albums.objects.get(id=album.id)
            a.name = album.name
            a.description = album.description
            a.backgroundImage = album.backgroundImage
            a.isActive = album.isActive
            a.updatedAt = now()
            a.save()
            return a
        except Exception:
            return None

    @staticmethod
    def delete(id):
        try:
            album = Albums.objects.get(id=id, isActive=True, deletedAt=None)
            album.isActive = False
            album.deletedAt = now()
            album.save()
            return album
        except Exception:
            return None 