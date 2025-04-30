from django.utils.timezone import now
from app.entities.genres import Genres

class GenresRepo:
    @staticmethod
    def getById(id):
        try:
            return Genres.objects.get(id=id, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def filterByName(name):
        try:
            return Genres.objects.filter(name__icontains=name, isActive=True, deletedAt=None)
        except Exception:
            return None

    @staticmethod
    def create(genre: Genres):
        try:
            return Genres.objects.create(
                id=genre.id,
                name=genre.name,
                description=genre.description,
                isActive=genre.isActive
            )
        except Exception:
            return None

    @staticmethod
    def update(genre: Genres):
        try:
            g = Genres.objects.get(id=genre.id)
            g.name = genre.name
            g.description = genre.description
            g.updatedAt = now()
            g.save()
            return g
        except Exception:
            return None

    @staticmethod
    def delete(id):
        try:
            genre = Genres.objects.get(id=id, isActive=True, deletedAt=None)
            genre.isActive = False
            genre.deletedAt = now()
            genre.save()
            return genre
        except Exception:
            return None 