from app.repositories.rolesRepo import RolesRepo
from datetime import datetime
from app.entities.roles import Roles
from common.errorCodes import ErrorCodes


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
    def findByName(name: str):
        if not name:
            return None, ErrorCodes.INVALID_INPUT
        role = RolesRepo.getByName(name)
        if not role:
            return None, ErrorCodes.NOT_FOUND
        return role, None

    @staticmethod
    def findAll():
        roles = RolesRepo.getAll()
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
    def doUpdate(role: Roles):
        id = role.id
        if not id:
            return None, ErrorCodes.INVALID_INPUT

        existing_role = RolesRepo.getById(id)
        if not existing_role:
            return None, ErrorCodes.NOT_FOUND

        if (role.name and RolesRepo.getByName(role.name)) and (existing_role.name != role.name):
            return None, ErrorCodes.ALREADY_EXISTS

        existing_role.name = role.name or existing_role.name
        existing_role.description = role.description or existing_role.description
        updated = RolesRepo.update(existing_role)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id: str):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        deleted = RolesRepo.delete(id)
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None 