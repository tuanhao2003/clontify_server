from app.repositories.songSubArtistRepo import SongSubArtistRepo
from app.grpc.grpcClients.usersGrpcClient import UsersGrpcClient
from app.services.songsService import SongsService
from app.entities.songSubArtist import SongSubArtist
from common.errorCodes import ErrorCodes
import uuid

class SongSubArtistService:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = SongSubArtistRepo.getAllPaginated(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            result = SongSubArtistRepo.getAll()
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findExactly(subArtistId: str, songId: str):
        try:
            result = SongSubArtistRepo.getExactly(uuid.UUID(subArtistId), uuid.UUID(songId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findByArtistIdPaginated(subArtistId: str, page: int = 1, pageSize: int = 10):
        try:
            result = SongSubArtistRepo.filterByArtistIdPaginated(uuid.UUID(subArtistId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByArtistId(subArtistId: str):
        try:
            result = SongSubArtistRepo.filterByArtistId(uuid.UUID(subArtistId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findBySongIdPaginated(songId: str, page: int = 1, pageSize: int = 10):
        try:
            result = SongSubArtistRepo.filterBySongIdPaginated(uuid.UUID(songId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findBySongId(songId: str):
        try:
            result = SongSubArtistRepo.filterBySongId(uuid.UUID(songId))
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def doCreate(subArtistId: str, songId: str):
        try:
            subArtistId = uuid.UUID(subArtistId)
            songId = uuid.UUID(songId)

            _, error = SongsService.findById(songId)
            if error:
                return None, error
            
            client = UsersGrpcClient()
            _, error = client.findById(subArtistId)
            client.close()
            if error:
                return None, error
            
            SongSubArtist = SongSubArtist(artistId=subArtistId, songId=songId)
            result = SongSubArtistRepo.create(SongSubArtist)
            if not result:
                return None, ErrorCodes.CREATE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doDelete(subArtistId: str, songId: str):
        try:
            subArtistId = uuid.UUID(subArtistId)
            songId = uuid.UUID(songId)

            _, error = SongsService.findById(songId)
            if error:
                return None, error
            
            client = UsersGrpcClient()
            _, error = client.findById(subArtistId)
            client.close()
            if error:
                return None, error
            
            SongSubArtist, error =  SongSubArtistService.findExactly(subArtistId, songId)
            if error:
                return None, error
            result = SongSubArtistRepo.delete(SongSubArtist)
            if not result:
                return None, ErrorCodes.DELETE_FAILED
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    