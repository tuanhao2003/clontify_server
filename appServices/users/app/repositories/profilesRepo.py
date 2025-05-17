from django.utils.timezone import now
from app.entities.profiles import Profiles
from datetime import datetime
import uuid


class ProfilesRepo:
    @staticmethod
    def getByID(id: uuid.UUID):
        try:
            return Profiles.objects.get(id=id, isActive=True)
        except Profiles.DoesNotExist:
            return None

    @staticmethod
    def getByIds(ids: list[uuid.UUID]):
        try:
            return Profiles.objects.filter(id__in=ids, isActive=True)
        except Exception:
            return None

    @staticmethod
    def getByAccountID(accountID: uuid.UUID):
        try:
            return Profiles.objects.get(accountID=accountID, isActive=True)
        except Profiles.DoesNotExist:
            return None

    @staticmethod
    def getByFullName(fullName: str):
        try:
            return Profiles.objects.get(fullName=fullName, isActive=True)
        except Profiles.DoesNotExist:
            return None

    @staticmethod
    def filterByDateOfBirth(date: datetime):
        try:
            if isinstance(date, str):
                date = datetime.fromisoformat(date)
            
            profiles = Profiles.objects.filter(
                dateOfBirth__year=date.year,
                dateOfBirth__month=date.month,
                dateOfBirth__day=date.day
            )
            return list(profiles)
        except Exception:
            return None

    @staticmethod
    def create(accountID: uuid.UUID, fullName: str, avatarUrl: str, bio: str, dateOfBirth: datetime, phoneNumber: str):
        try:
            return Profiles.objects.create(
                accountID=accountID,
                fullName=fullName,
                avatarUrl=avatarUrl,
                bio=bio,
                dateOfBirth=dateOfBirth,
                phoneNumber=phoneNumber
            )
        except Exception:
            return None

    @staticmethod
    def update(profile: Profiles):
        try:
            prof = Profiles.objects.get(id=profile.id, isActive=True)
            prof.fullName = profile.fullName
            prof.avatarUrl = profile.avatarUrl
            prof.bio = profile.bio
            prof.dateOfBirth = profile.dateOfBirth
            prof.phoneNumber = profile.phoneNumber
            prof.updatedAt = now()
            prof.save()
            return prof
        except Profiles.DoesNotExist:
            return None

    @staticmethod
    def delete(id: uuid.UUID):
        try:
            profile = Profiles.objects.get(id=id, isActive=True)
            profile.deletedAt = now()
            profile.save()
            return profile
        except Exception:
            return None
