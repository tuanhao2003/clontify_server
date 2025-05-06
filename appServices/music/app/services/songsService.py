from app.repositories.songsRepo import SongsRepo
from app.entities.songs import Songs
from common.errorCodes import ErrorCodes
import uuid
from app.services.genreSongService import GenreSongService
from app.services.albumSongService import AlbumSongService
from app.services.songSubArtistService import SongSubArtistService
class SongsService:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.findAllPaginated(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            result = SongsRepo.findAll()
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
    def findByIds(ids: list[str]):
        try:
            if not ids:
                return None, ErrorCodes.INVALID_INPUT
            uuids = [uuid.UUID(id) for id in ids]
            songs = SongsRepo.getByIds(uuids)
            if not songs:
                return None, ErrorCodes.NOT_FOUND
            return songs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByTitlePaginated(title: str, page: int = 1, pageSize: int = 10):
        try:
            if not title or title == "":
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.filterByTitlePaginated(title, page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByTitle(title: str):
        try:
            if not title or title == "":
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.filterByTitle(title)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByGenreId(genreId: str):
        try:
            if not genreId or genreId == "":
                return None, ErrorCodes.INVALID_INPUT
            songIds = GenreSongService.findByGenreId(genreId)
            if not songIds:
                return None, ErrorCodes.NOT_FOUND
            songs = SongsRepo.findByIds(songIds)
            if not songs:
                return None, ErrorCodes.NOT_FOUND
            return songs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
                
    @staticmethod
    def findByGenreIdPaginated(genreId: str, page: int = 1, pageSize: int = 10):
        try:
            if not genreId or genreId == "":
                return None, ErrorCodes.INVALID_INPUT
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
                
            genreSongs, error = GenreSongService.findByGenreIdPaginated(genreId, page, pageSize)
            if error:
                return None, error
            if not genreSongs:
                return None, ErrorCodes.NOT_FOUND
                
            songIds = [str(genreSong.songId) for genreSong in genreSongs['result']]
            songs = SongsRepo.findByIds(songIds)
            if not songs:
                return None, ErrorCodes.NOT_FOUND
                
            return {
                'result': songs,
                'total': genreSongs['total'],
                'totalPages': genreSongs['totalPages'],
                'currentPage': genreSongs['currentPage']
            }, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
                
    @staticmethod
    def findByAlbumId(albumId: str):
        try:
            if not albumId or albumId == "":
                return None, ErrorCodes.INVALID_INPUT
            songIds = AlbumSongService.findByAlbumId(albumId)
            if not songIds:
                return None, ErrorCodes.NOT_FOUND
            songs = SongsRepo.findByIds(songIds)
            if not songs:
                return None, ErrorCodes.NOT_FOUND
            return songs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
            
    @staticmethod
    def findByAlbumIdPaginated(albumId: str, page: int = 1, pageSize: int = 10):
        try:
            if not albumId or albumId == "":
                return None, ErrorCodes.INVALID_INPUT
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
                
            albumSongs, error = AlbumSongService.findByAlbumIdPaginated(albumId, page, pageSize)
            if error:
                return None, error
            if not albumSongs:
                return None, ErrorCodes.NOT_FOUND
                
            songIds = [str(albumSong.songId) for albumSong in albumSongs['result']]
            songs = SongsRepo.findByIds(songIds)
            if not songs:
                return None, ErrorCodes.NOT_FOUND
                
            return {
                'result': songs,
                'total': albumSongs['total'],
                'totalPages': albumSongs['totalPages'],
                'currentPage': albumSongs['currentPage']
            }, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    @staticmethod
    def findByArtistIdPaginated(artistId: str, page: int = 1, pageSize: int = 10):
        try:
            if not artistId or artistId == "":
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.filterByArtistIdPaginated(uuid.UUID(artistId), page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findByArtistId(artistId: str):
        try:
            if not artistId or artistId == "":
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.filterByArtistId(uuid.UUID(artistId))
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
                AlbumSongService.doCreate(uuid.UUID(id), songId)
            if genreIds:
                for id in genreIds:
                    GenreSongService.doCreate(uuid.UUID(id), songId)

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
            if error:
                return None, error
            if albumSongs:
                for albumSong in albumSongs:
                    _, error = AlbumSongService.doDelete(str(albumSong.albumId), str(albumSong.songId))
                    if error:
                        return None, error

            genreSongs, error = GenreSongService.findBySongId(id)
            if error:
                return None, error
            if genreSongs:
                for genreSong in genreSongs:
                    _, error = GenreSongService.doDelete(str(genreSong.genreId), str(genreSong.songId))
                    if error:
                        return None, error
                    
            songSubArtists, error = SongSubArtistService.findBySongId(id)
            if error:
                return None, error
            if songSubArtists:
                for songSubArtist in songSubArtists:
                    _, error = SongSubArtistService.doDelete(str(songSubArtist.songId), str(songSubArtist.subArtistId))
                    if error:
                        return None, error

            deleted = SongsRepo.delete(currentSong)
            if not deleted:
                return None, ErrorCodes.DELETE_FAILED
            return deleted, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
