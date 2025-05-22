from app.repositories.accountsRepo import AccountsRepo
from datetime import datetime
from app.entities.accounts import Accounts
from common.errorCodes import ErrorCodes
from django.contrib.auth.hashers import make_password

class AccountsService:

    @staticmethod
    def findAll():
        accounts = AccountsRepo.filterAll()
        if not accounts:
            return None, ErrorCodes.NOT_FOUND
        return accounts, None

    @staticmethod
    def findAllPaginated(page: int, pageSize: int):
        accounts = AccountsRepo.filterAllPaginated(page, pageSize)
        if not accounts:
            return None, ErrorCodes.NOT_FOUND
        return accounts, None

    @staticmethod
    def findById(id: str):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        account = AccountsRepo.getById(id)
        if not account:
            return None, ErrorCodes.NOT_FOUND
        return account, None

    @staticmethod
    def findByUsername(username: str):
        if not username:
            return None, ErrorCodes.INVALID_INPUT
        account = AccountsRepo.getByUsername(username)
        if not account:
            return None, ErrorCodes.NOT_FOUND
        return account, None

    @staticmethod
    def findByEmail(email: str):
        if not email:
            return None, ErrorCodes.INVALID_INPUT
        account = AccountsRepo.getByEmail(email)
        if not account:
            return None, ErrorCodes.NOT_FOUND
        return account, None

    @staticmethod
    def findByStatus(status: bool):
        if not status:
            return None, ErrorCodes.INVALID_STATUS
        accounts = AccountsRepo.filterByStatus(status)
        if not accounts:
            return None, ErrorCodes.NOT_FOUND
        return accounts, None

    @staticmethod
    def findByDateCreated(start: datetime, end: datetime):
        if (not start or not end) or (start > end):
            return None, ErrorCodes.INVALID_INPUT
        accounts = AccountsRepo.filterByDateCreated(start, end)
        if not accounts or len(accounts) == 0:
            return None, ErrorCodes.NOT_FOUND
        return accounts, None

    @staticmethod
    def doCreate(username: str, email: str, password: str, roleId: str):
        if not username or not email or not password or not roleId:
            return None, ErrorCodes.INVALID_INPUT
        if AccountsRepo.getByUsername(username):
            return None, ErrorCodes.ALREADY_EXISTS
        if AccountsRepo.getByEmail(email):
            return None, ErrorCodes.ALREADY_EXISTS
        account = Accounts(
            username=username,
            email=email,
            password=password,
            roleId=roleId,
            isActive=True,
        )
        created = AccountsRepo.create(account)
        if not created:
            return None, ErrorCodes.CREATE_FAILED
        return created, None

    @staticmethod
    def doUpdate(account: Accounts):
        id = account.id
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        existingAccount = AccountsRepo.getById(id)
        if not existingAccount:
            return None, ErrorCodes.NOT_FOUND
        if (account.email and AccountsRepo.getByEmail(account.email)) and (existingAccount.email != account.email):
            return None, ErrorCodes.ALREADY_EXISTS
        existingAccount.email = account.email or existingAccount.email
        existingAccount.password = make_password(account.password) or existingAccount.password
        if account.roleId:
            existingAccount.roleId = account.roleId
        updated = AccountsRepo.update(existingAccount)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id: str):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        deleted = AccountsRepo.delete(id)
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None