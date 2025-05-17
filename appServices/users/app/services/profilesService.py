from app.repositories.profilesRepo import ProfilesRepo
from datetime import datetime
from app.entities.profiles import Profiles
import uuid
from common.errorCodes import ErrorCodes


class ProfilesService:
    @staticmethod
    def findByID(id: str):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        try:
            profileId = uuid.UUID(id)
        except ValueError:
            return None, ErrorCodes.INVALID_INPUT
            
        profile = ProfilesRepo.getByID(profileId)
        if not profile:
            return None, ErrorCodes.NOT_FOUND
        return profile, None
    
    @staticmethod
    def findByIds(ids: list[str]):
        if not ids or len(ids) == 0:
            return None, ErrorCodes.INVALID_INPUT
            
        profiles = ProfilesRepo.getByIds([uuid.UUID(id) for id in ids])
        if not profiles:
            return None, ErrorCodes.NOT_FOUND
        return profiles, None

    @staticmethod 
    def findByAccountID(accountID: str):
        if not accountID:
            return None, ErrorCodes.INVALID_INPUT
        try:
            accountId = uuid.UUID(accountID)
        except ValueError:
            return None, ErrorCodes.INVALID_INPUT

        profile = ProfilesRepo.getByAccountID(accountId)
        if not profile:
            return None, ErrorCodes.NOT_FOUND
        return profile, None

    @staticmethod
    def findByFullName(fullName: str):
        if not fullName:
            return None, ErrorCodes.INVALID_INPUT
        profile = ProfilesRepo.getByFullName(fullName)
        if not profile:
            return None, ErrorCodes.NOT_FOUND
        return profile, None

    @staticmethod
    def findByDateOfBirth(date: datetime):
        if not date:
            return None, ErrorCodes.INVALID_INPUT
        try:
            birthDate = datetime.fromisoformat(date) if isinstance(date, str) else date
            profiles = ProfilesRepo.filterByDateOfBirth(birthDate)
            if not profiles or len(profiles) == 0:
                return None, ErrorCodes.NOT_FOUND
            return profiles, None
        except ValueError:
            return None, ErrorCodes.INVALID_INPUT

    @staticmethod
    def doCreate(accountID: str, fullName: str, avatarUrl: str = None, bio: str = None, dateOfBirth: datetime = None, phoneNumber: str = None):
        if not accountID or not fullName:
            return None, ErrorCodes.INVALID_INPUT
            
        try:
            accountId = uuid.UUID(accountID)
        except ValueError:
            return None, ErrorCodes.INVALID_INPUT

        if ProfilesRepo.getByAccountID(accountId):
            return None, ErrorCodes.ALREADY_EXISTS

        created = ProfilesRepo.create(accountID, fullName, avatarUrl, bio, dateOfBirth, phoneNumber)
        if not created:
            return None, ErrorCodes.CREATE_FAILED
        return created, None

    @staticmethod
    def doUpdate(profile: Profiles):
        id = profile.id
        if not id:
            return None, ErrorCodes.INVALID_INPUT

        prof = ProfilesRepo.getByID(id)
        if not prof:
            return None, ErrorCodes.NOT_FOUND

        prof.fullName = profile.fullName or prof.fullName
        prof.avatarUrl = profile.avatarUrl or prof.avatarUrl
        prof.bio = profile.bio or prof.bio
        prof.dateOfBirth = profile.dateOfBirth or prof.dateOfBirth
        prof.phoneNumber = profile.phoneNumber or prof.phoneNumber
        
        updated = ProfilesRepo.update(prof)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id: str):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        try:
            profileId = uuid.UUID(id)
        except ValueError:
            return None, ErrorCodes.INVALID_INPUT
            
        deleted = ProfilesRepo.delete(profileId)
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None
