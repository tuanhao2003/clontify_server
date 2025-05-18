from app.repositories.rolesRepo import RolesRepo
from datetime import datetime
from app.entities.roles import Roles
from common.errorCodes import ErrorCodes
import uuid


class RolesService:
    @staticmethod
    def findById(id: str):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        role = RolesRepo.getById(id)
        if not role:
            return None, ErrorCodes.NOT_FOUND
        return role, None
    
    @staticmethod
    def findByIds(ids: list[str]):
        if not ids:
            return None, ErrorCodes.INVALID_INPUT
        listUUID = [uuid.UUID(id) for id in ids]
        role = RolesRepo.getByIds(listUUID)
        if not role:
            return None, ErrorCodes.NOT_FOUND
        return role, None

    @staticmethod
    def findByName(name: str):
        if not name:
            return None, ErrorCodes.INVALID_INPUT
        roles = RolesRepo.filterByName(name)
        if not roles:
            return None, ErrorCodes.NOT_FOUND
        return roles, None
    @staticmethod
    def findByNamePaginated(name: str, page: int = 1, pageSize: int = 10):
        if not name:
            return None, ErrorCodes.INVALID_INPUT
        roles = RolesRepo.filterByNamePaginated(name, page, pageSize)
        if not roles:
            return None, ErrorCodes.NOT_FOUND
        return roles, None

    @staticmethod
    def findAll():
        roles = RolesRepo.filterAll()
        if not roles or len(roles) == 0:
            return None, ErrorCodes.NOT_FOUND
        return roles, None
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        roles = RolesRepo.filterAllPaginated(page, pageSize)
        if not roles or len(roles) == 0:
            return None, ErrorCodes.NOT_FOUND
        return roles, None

    @staticmethod
    def doCreate(name: str, description: str = None):
        if not name:
            return None, ErrorCodes.INVALID_INPUT

        if RolesRepo.getByName(name):
            return None, ErrorCodes.ALREADY_EXISTS

        role = Roles(
            name=name,
            description=description
        )
        created = RolesRepo.create(role)
        if not created:
            return None, ErrorCodes.CREATE_FAILED
        return created, None

    @staticmethod
    def doUpdate(id: str, name: str = None, description: str = None):
        if not id:
            return None, ErrorCodes.INVALID_INPUT

        existingRole = RolesRepo.getByID(uuid.UUID(id))
        if not existingRole:
            return None, ErrorCodes.NOT_FOUND

        if (name and RolesRepo.filterByName(name)) and (existingRole.name != name):
            return None, ErrorCodes.ALREADY_EXISTS

        existingRole.name = name or existingRole.name
        existingRole.description = description or existingRole.description
        updated = RolesRepo.update(existingRole)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id: str):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        deleted = RolesRepo.delete(uuid.UUID(id))
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None 