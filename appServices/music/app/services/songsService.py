from app.repositories.songsRepo import SongsRepo
from app.repositories.songSubArtistRepo import SongSubArtistRepo
from app.entities.songs import Songs
from common.errorCodes import ErrorCodes
import uuid
from app.services.genreSongService import GenreSongService
from app.services.albumSongService import AlbumSongService
from app.enums.songTypes import SongTypes
from app.services.albumsService import AlbumsService
from app.services.genresService import GenresService

class SongsService:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.filterAllPaginated(page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findAll():
        try:
            result = SongsRepo.filterAll()
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
            songs = SongsRepo.getByIds(songIds)
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
            songs = SongsRepo.getByIds(songIds)
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
            songs = SongsRepo.getByIds(songIds)
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
            songs = SongsRepo.getByIds(songIds)
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
    def doCreate(title: str, artistId: str, storageId: str, albumIds: list[str], songType: str, genreIds: list[str] = None, storageImageId: str = None, duration: int = None, description: str = None, subArtistIds: list[str] = None):
        try:            
            if not title or not artistId or not albumIds or not storageId or not songType or title == "" or artistId == "" or albumIds == [] or storageId == "" or songType == "":
                return None, ErrorCodes.INVALID_INPUT
            
            try:
                song = Songs(
                    title=title,
                    artistId=uuid.UUID(artistId),
                    storageId=uuid.UUID(storageId),
                    storageImageId=uuid.UUID(storageImageId) if storageImageId else None,
                    duration=duration,
                    description=description,
                    songType=SongTypes[songType]
                )
            except Exception:
                return None, ErrorCodes.INVALID_INPUT
            
            try:
                song = SongsRepo.create(song)
                if not song:
                    return None, ErrorCodes.CREATE_FAILED
            except Exception:
                return None, ErrorCodes.CREATE_FAILED
            
            songId = str(song.id)
            for id in albumIds:
                albumExists, _ = AlbumsService.findById(id)
                if albumExists:
                    AlbumSongService.doCreate(albumId=id, songId=songId)
                else:
                    pass
            
            if genreIds:
                for id in genreIds:
                    genreExists, _ = GenresService.findById(id)
                    if genreExists:
                        GenreSongService.doCreate(genreId=id, songId=songId)
                    else:
                        pass

            return song, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def doUpdate(id: str, title: str = None, storageImageId: str = None, duration: int = None, description: str = None, songType: str = None):
        try:
            if not id or id == "":
                return None, ErrorCodes.INVALID_INPUT
                
            currentSong = SongsRepo.getById(uuid.UUID(id))
            if not currentSong:
                return None, ErrorCodes.NOT_FOUND

            if title is not None:
                currentSong.title = title
            if storageImageId is not None:
                currentSong.storageImageId = uuid.UUID(storageImageId) if storageImageId else None
            if duration is not None:
                currentSong.duration = duration
            if description is not None:
                currentSong.description = description
            if songType is not None:
                currentSong.songType = SongTypes[songType]               

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
            currentSong, error = SongsService.findById(id)
            if error:
                return None, error

            albumSongs, error = AlbumSongService.findBySongId(id)
            if error:
                return None, error
            if albumSongs:
                for albumSong in albumSongs:
                    AlbumSongService.doDelete(str(albumSong.albumId), str(albumSong.songId))

            genreSongs, error = GenreSongService.findBySongId(id)
            if error:
                return None, error
            if genreSongs:
                for genreSong in genreSongs:
                    GenreSongService.doDelete(str(genreSong.genreId), str(genreSong.songId))
                    
            songSubArtists = SongSubArtistRepo.filterBySongId(uuid.UUID(id))
            if songSubArtists:
                for songSubArtist in songSubArtists:
                    SongSubArtistRepo.delete(songSubArtist)

            deleted = SongsRepo.delete(currentSong)
            if not deleted:
                return None, ErrorCodes.DELETE_FAILED
            return deleted, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findBySongType(songType: str):
        try:
            if not songType or songType == "":
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.filterBySongType(SongTypes[songType])
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def findBySongTypePaginated(songType: str, page: int = 1, pageSize: int = 10):
        try:
            if not songType or songType == "":
                return None, ErrorCodes.INVALID_INPUT
            if not page or not pageSize:
                return None, ErrorCodes.INVALID_INPUT
            result = SongsRepo.filterBySongTypePaginated(SongTypes[songType], page, pageSize)
            if not result:
                return None, ErrorCodes.NOT_FOUND
            return result, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED