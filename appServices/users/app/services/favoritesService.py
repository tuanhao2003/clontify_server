from app.repositories.favoritesRepo import FavoritesRepo
from app.grpc.grpcClients.musicGrpcClient import MusicGrpcClient
from app.services.profilesService import ProfilesService
from app.entities.favorites import Favorites
from common.errorCodes import ErrorCodes
import uuid

class FavoritesService:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = FavoritesRepo.filterAllPaginated(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            result = FavoritesRepo.filterAll()
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findExactly(profileId: str, songId: str):
        try:
            result = FavoritesRepo.getExactly(uuid.UUID(profileId), uuid.UUID(songId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findByProfileIdPaginated(profileId: str, page: int = 1, pageSize: int = 10):
        try:
            result = FavoritesRepo.filterByProfileIdPaginated(uuid.UUID(profileId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByProfileId(profileId: str):
        try:
            result = FavoritesRepo.filterByProfileId(uuid.UUID(profileId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findBySongIdPaginated(songId: str, page: int = 1, pageSize: int = 10):
        try:
            result = FavoritesRepo.filterBySongIdPaginated(uuid.UUID(songId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findBySongId(songId: str):
        try:
            result = FavoritesRepo.filterBySongId(uuid.UUID(songId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def doCreate(profileId: str, songId: str):
        try:
            profileId = uuid.UUID(profileId)
            songId = uuid.UUID(songId)

            _, error = ProfilesService.findByID(str(profileId))
            if error:
                return None, error

            musicClient = MusicGrpcClient()
            try:
                song, error = musicClient.getSongById(str(songId))
                if error:
                    return None, ErrorCodes.NOT_FOUND
                
                favorite = Favorites(profileID=profileId, songID=songId)
                result = FavoritesRepo.create(favorite)
                if not result:
                    return None, ErrorCodes.CREATE_FAILED
                return result, None
            finally:
                musicClient.close()
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDelete(profileId: str, songId: str):
        try:
            profileId = uuid.UUID(profileId)
            songId = uuid.UUID(songId)

            _, error = ProfilesService.findByID(str(profileId))
            if error:
                return None, error

        
            musicClient = MusicGrpcClient()
            try:
                song, error = musicClient.getSongById(str(songId))
                if error or not song:
                    return None, ErrorCodes.NOT_FOUND
                
                favorite, error = FavoritesService.findExactly(str(profileId), str(songId))
                if error:
                    return None, error
                result = FavoritesRepo.delete(favorite)
                if not result:
                    return None, ErrorCodes.DELETE_FAILED
                return result, None
            finally:
                musicClient.close()
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED 