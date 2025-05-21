from app.entities.roles import Roles
from django.core.paginator import Paginator
import uuid
from django.utils.timezone import now
class RolesRepo:
    @staticmethod
    def getByID(id: uuid.UUID):
        try:
            return Roles.objects.get(id=id)
        except Roles.DoesNotExist:
            return None
        
    @staticmethod
    def getByIds(ids: list[uuid.UUID]):
        try:
            return Roles.objects.filter(id__in=ids, isActive=True)
        except Exception:
            return None
        
    @staticmethod
    def filterByNamePaginated(name: str, page: int = 1, pageSize: int = 10):
        try:
            result = Roles.objects.filter(name__icontains=name, isActive=True)
            paginator = Paginator(result, pageSize)
            return {
                'result': paginator,
                'total': paginator.count,
                'totalPages': paginator.num_pages,
                'currentPage': page
            }
        except Exception:
            return None

    @staticmethod
    def filterByName(name: str):
        try:
            return Roles.objects.get(name__icontains=name)
        except Roles.DoesNotExist:
            return None

    @staticmethod
    def filterAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = Roles.objects.filter(isActive=True)
            paginator = Paginator(result, pageSize)
            return {
                'result':paginator,
                'total':paginator.count,
                'totalPages':paginator.num_pages,
                'currentPage': page
            }
        except Exception:
            return None

    @staticmethod
    def filterAll():
        try:
            return Roles.objects.all()
        except Exception:
            return None

    @staticmethod
    def create(role: Roles):
        try:
            role.save()
            return role
        except Exception:
            return None

    @staticmethod
    def update(role: Roles):
        try:
            role.save()
            role.updatedAt = now()
            return role
        except Exception:
            return None

    @staticmethod
    def delete(role: Roles):
        try:
            role.isActive = False
            role.deletedAt = now()
            role.save()
            return role
        except Exception:
            return None 