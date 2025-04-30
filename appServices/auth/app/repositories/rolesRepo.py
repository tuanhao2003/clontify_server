from app.entities.roles import Roles

class RolesRepo:
    @staticmethod
    def getByID(id: str):
        try:
            return Roles.objects.get(id=id)
        except Roles.DoesNotExist:
            return None

    @staticmethod
    def getByName(name: str):
        try:
            return Roles.objects.get(name=name)
        except Roles.DoesNotExist:
            return None

    @staticmethod
    def getAll():
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
            return role
        except Exception:
            return None

    @staticmethod
    def delete(id: str):
        try:
            role = Roles.objects.get(id=id)
            role.delete()
            return True
        except Exception:
            return False 