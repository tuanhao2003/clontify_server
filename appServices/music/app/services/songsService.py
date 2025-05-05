from app.repositories.songsRepo import SongsRepo
from app.entities.songs import Songs
from common.errorCodes import ErrorCodes
import uuid
from app.services.genreSongService import GenreSongService
from app.services.albumSongService import AlbumSongService
class SongsService:
    @staticmethod
    def findAll(page: int = 1, pageSize: int = 10):
        try:
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.findAll(page, pageSize)
            if not result:
                    return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
        
    @staticmethod
    def findById(id: str):
        try:
            if not id:
                return None, ErrorCodes.INVALID_INPUT
            
            song = SongsRepo.getById(uuid.UUID(id))
            if not song:
                return None, ErrorCodes.NOT_FOUND
            return song, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByTitle(title: str, page: int = 1, pageSize: int = 10):
        try:
            if not title or title == "":
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.filterByTitle(title, page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

# grpc
    # @staticmethod
    # def findByArtistId(artistId: str):
    #     try:
    #         if not artistId or artistId == "":
    #             return None, ErrorCodes.INVALID_INPUT
    #         songIds = ArtistSongService.getByArtistId(artistId)
    #         if not songIds:
    #             return None, ErrorCodes.NOT_FOUND
    #         songs = SongsRepo.getByIds(songIds)
    #         if not songs:
    #             return None, ErrorCodes.NOT_FOUND
    #         return songs, None
    #     except Exception:
    #         return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByGenreId(genreId: str):
        try:
            if not genreId or genreId == "":
                return None, ErrorCodes.INVALID_INPUT
            songIds = GenreSongService.getByGenreId(genreId)
            if not songIds:
                return None, ErrorCodes.NOT_FOUND
            songs = SongsRepo.getByIds(songIds)
            if not songs:
                return None, ErrorCodes.NOT_FOUND
            return songs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
                

    @staticmethod
    def findByAlbumId(albumId: str):
        try:
            if not albumId or albumId == "":
                return None, ErrorCodes.INVALID_INPUT
            songIds = AlbumSongService.getByAlbumId(albumId)
            if not songIds:
                return None, ErrorCodes.NOT_FOUND
            songs = SongsRepo.getByIds(songIds)
            if not songs:
                return None, ErrorCodes.NOT_FOUND
            return songs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    @staticmethod
    def findByArtistId(artistId: str, page: int = 1, pageSize: int = 10):
        try:
            if not artistId or artistId == "":
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.filterByArtistId(uuid.UUID(artistId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    @staticmethod
    def doCreate(title: str, artistId: str, audioUrl: str, albumIds: list[str], genreIds: list[str] = None, backgroundImage: str = None, duration: int = None, description: str = None, subArtistIds: list[str] = None):
        try:
            if not title or not artistId or not albumIds or not audioUrl or title == "" or artistId == "" or albumIds == [] or audioUrl == "":
                return None, ErrorCodes.INVALID_INPUT
            song = Songs(
                title=title,
                description=description,
                audioUrl=audioUrl,
                backgroundImage=backgroundImage,
                duration=duration,
                isActive=False
            )
            songId = SongsRepo.create(song)
            if not songId:
                return None, ErrorCodes.CREATE_FAILED
            for id in albumIds:
                AlbumSongService.create(uuid.UUID(id), songId)
            if genreIds:
                for id in genreIds:
                    GenreSongService.create(uuid.UUID(id), songId)

            # ArtistSongService.create(artistId, songId) grpc
            return songId, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doUpdate(id: str, title: str = None, backgroundImage: str = None, duration: int = None, description: str = None):
        try:
            if not id or id == "":
                return None, ErrorCodes.INVALID_INPUT
                
            currentSong = SongsRepo.getById(uuid.UUID(id))
            if not currentSong:
                return None, ErrorCodes.NOT_FOUND

            if title is not None:
                currentSong.title = title
            if backgroundImage is not None:
                currentSong.backgroundImage = backgroundImage
            if duration is not None:
                currentSong.duration = duration
            if description is not None:
                currentSong.description = description                

            updated = SongsRepo.update(currentSong)
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
            currentSong = SongsRepo.getById(uuid.UUID(id))
            if not currentSong:
                return None, ErrorCodes.NOT_FOUND
            albumSongs, error = AlbumSongService.findBySongId(id)
            if albumSongs and albumSongs['result']:
                for albumSong in albumSongs['result']:
                    AlbumSongService.doDelete(str(albumSong.albumId), str(albumSong.songId))

            genreSongs, error = GenreSongService.findBySongId(id)
            if genreSongs and genreSongs['result']:
                for genreSong in genreSongs['result']:
                    GenreSongService.doDelete(str(genreSong.genreId), str(genreSong.songId))

            deleted = SongsRepo.delete(currentSong)
            if not deleted:
                return None, ErrorCodes.DELETE_FAILED
            return deleted, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
