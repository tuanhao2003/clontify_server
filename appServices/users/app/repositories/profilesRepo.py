from django.utils.timezone import now
from app.entities.profiles import Profiles
from datetime import datetime
import uuid


class ProfilesRepo:
    @staticmethod
    def getByID(id: uuid.UUID):
        try:
            return Profiles.objects.get(id=id)
        except Profiles.DoesNotExist:
            return None

    @staticmethod
    def getByAccountID(accountID: uuid.UUID):
        try:
            return Profiles.objects.get(accountID=accountID)
        except Profiles.DoesNotExist:
            return None

    @staticmethod
    def getByFullName(fullName: str):
        try:
            return Profiles.objects.get(fullName=fullName)
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
    def create(profile: Profiles):
        try:
            return Profiles.objects.create(
                accountID=profile.accountID,
                fullName=profile.fullName,
                avatarUrl=profile.avatarUrl,
                bio=profile.bio,
                dateOfBirth=profile.dateOfBirth,
                phoneNumber=profile.phoneNumber
            )
        except Exception:
            return None

    @staticmethod
    def update(profile: Profiles):
        try:
            prof = Profiles.objects.get(id=profile.id)
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
            profile = Profiles.objects.get(id=id)
            profile.deletedAt = now()
            profile.save()
            return profile
        except Exception:
            return None
