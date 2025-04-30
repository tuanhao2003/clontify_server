from app.repositories.songsRepo import SongsRepo
from app.entities.songs import Songs
from common.errorCodes import ErrorCodes

class SongsService:
    @staticmethod
    def findById(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        song = SongsRepo.getById(id)
        if not song:
            return None, ErrorCodes.NOT_FOUND
        return song, None

    @staticmethod
    def findByTitle(title):
        if not title:
            return None, ErrorCodes.INVALID_INPUT
        songs = SongsRepo.getByTitle(title)
        if not songs:
            return None, ErrorCodes.NOT_FOUND
        return songs, None

    @staticmethod
    def findByArtistId(artistId):
        if not artistId:
            return None, ErrorCodes.INVALID_INPUT
        songs = SongsRepo.filterByArtistId(artistId)
        if not songs:
            return None, ErrorCodes.NOT_FOUND
        return songs, None

    @staticmethod
    def findByGenreId(genreId):
        if not genreId:
            return None, ErrorCodes.INVALID_INPUT
        songs = SongsRepo.filterByGenreId(genreId)
        if not songs:
            return None, ErrorCodes.NOT_FOUND
        return songs, None

    @staticmethod
    def doCreate(title, artistId, genreId, audioUrl, backgroundImage=None, duration=None, releaseDate=None):
        if not title or not artistId or not genreId or not audioUrl:
            return None, ErrorCodes.INVALID_INPUT
        existing = SongsRepo.getByTitle(title)
        if existing and existing.exists():
            return None, ErrorCodes.ALREADY_EXISTS
        song = Songs(
            title=title,
            artistId=artistId,
            genreId=genreId,
            audioUrl=audioUrl,
            backgroundImage=backgroundImage,
            duration=duration,
        )
        created = SongsRepo.create(song)
        if not created:
            return None, ErrorCodes.CREATE_FAILED
        return created, None

    @staticmethod
    def doUpdate(song: Songs):
        if not song.id:
            return None, ErrorCodes.INVALID_INPUT
        updated = SongsRepo.update(song)
        if not updated:
            return None, ErrorCodes.UPDATE_FAILED
        return updated, None

    @staticmethod
    def doDelete(id):
        if not id:
            return None, ErrorCodes.INVALID_INPUT
        deleted = SongsRepo.delete(id)
        if not deleted:
            return None, ErrorCodes.DELETE_FAILED
        return deleted, None 