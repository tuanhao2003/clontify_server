from django.utils.timezone import now
from app.entities.accounts import Accounts
from datetime import datetime
import uuid


class AccountsRepo:
    @staticmethod
    def getByID(id: uuid.uuid4):
        try:
            return Accounts.objects.get(id=id)
        except Accounts.DoesNotExist:
            return None

    @staticmethod
    def getByEmail(email: str):
        try:
            return Accounts.objects.get(email=email)
        except Accounts.DoesNotExist:
            return None

    @staticmethod
    def getByUsername(un: str):
        try:
            return Accounts.objects.get(username=un)
        except Accounts.DoesNotExist:
            return None

    @staticmethod
    def filterByStatus(status: bool):
        try:
            return Accounts.objects.filter(isActive=status)
        except Exception:
            return None

    @staticmethod
    def filterByDateCreated(startDate: datetime, endDate: datetime):
        try:
            return Accounts.objects.filter(createAt__range=(startDate, endDate))
        except Exception:
            return None

    @staticmethod
    def create(account: Accounts):
        try:
            return Accounts.objects.create(account)
        except Exception:
            return None

    @staticmethod
    def update(account: Accounts):
        try:
            acc = Accounts.objects.get(id=account.id)
            acc.email = account.email
            acc.password = account.password
            acc.updatedAt = now()
            acc.save()
            return acc
        except Accounts.DoesNotExist:
            return None


    @staticmethod
    def delete(id: uuid.uuid4):
        try:
            account = Accounts.objects.get(id=id)
            account.deletedAt = now()
            account.isActive = False
            account.save()
            return account
        except Exception:
            return None
