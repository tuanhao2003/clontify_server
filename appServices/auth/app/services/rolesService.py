from app.repositories.rolesRepo import RolesRepo
from datetime import datetime
from app.entities.roles import Roles
from common.errorCodes import ErrorCodes
import uuid


class RolesService:
    @staticmethod
    def findById(id: str):
        try:
            if not id:
                return None, ErrorCodes.INVALID_INPUT
            role = RolesRepo.getById(id)
            if not role:
                return None, ErrorCodes.NOT_FOUND
            return role, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findByIds(ids: list[str]):
        try:
            if not ids:
                return None, ErrorCodes.INVALID_INPUT
            listUUID = [uuid.UUID(id) for id in ids]
            role = RolesRepo.getByIds(listUUID)
            if not role:
                return None, ErrorCodes.NOT_FOUND
            return role, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByName(name: str):
        try:
            if not name:
                return None, ErrorCodes.INVALID_INPUT
            roles = RolesRepo.filterByName(name)
            if not roles:
                return None, ErrorCodes.NOT_FOUND
            return roles, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findByNamePaginated(name: str, page: int = 1, pageSize: int = 10):
        try:
            if not name:
                return None, ErrorCodes.INVALID_INPUT
            roles = RolesRepo.filterByNamePaginated(name, page, pageSize)
            if not roles:
                return None, ErrorCodes.NOT_FOUND
            return roles, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            roles = RolesRepo.filterAll()
            if not roles or len(roles) == 0:
                return None, ErrorCodes.NOT_FOUND
            return roles, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            roles = RolesRepo.filterAllPaginated(page, pageSize)
            if not roles or len(roles) == 0:
                return None, ErrorCodes.NOT_FOUND
            return roles, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def doCreate(name: str, description: str = None):
        try:
            if not name:
                return None, ErrorCodes.INVALID_INPUT

            if RolesRepo.filterByName(name):
                return None, ErrorCodes.ALREADY_EXISTS

            role = Roles(
                name=name,
                description=description
            )
            created = RolesRepo.create(role)
            if not created:
                return None, ErrorCodes.CREATE_FAILED
            return created, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doUpdate(id: str, name: str = None, description: str = None):
        try:
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
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDelete(id: str):
        try:
            if not id:
                return None, ErrorCodes.INVALID_INPUT
            currentRole = RolesRepo.getByID(uuid.UUID(id))
            if not currentRole:
                    return None, ErrorCodes.NOT_FOUND
            deleted = RolesRepo.delete(currentRole)
            if not deleted:
                return None, ErrorCodes.DELETE_FAILED
            return deleted, None 
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDeleteMany(ids: list[str]) -> tuple[list[Roles], int]:
        try:
            if not ids or len(ids) == 0:
                return None, ErrorCodes.INVALID_INPUT
            result = []
            for i in ids:
                currentRole = RolesRepo.getByID(uuid.UUID(i))
                if not currentRole:
                    return None, ErrorCodes.NOT_FOUND
                deleted = RolesRepo.delete(currentRole)
                if not deleted:
                    return None, ErrorCodes.DELETE_FAILED
                result.append(deleted)
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED