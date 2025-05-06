import grpc
from concurrent import futures
import time
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import musicService_pb2, musicService_pb2_grpc
from app.services.songsService import SongsService
from app.services.albumsService import AlbumsService
from app.services.genresService import GenresService
from common.errorCodes import ErrorCodes

class MusicGrpc(musicService_pb2_grpc.MusicServiceServicer):
    def _parseTimestamp(self, dt):
        if not dt or not isinstance(dt, datetime):
            return None
        timestamp = Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp
    
    def _parseDatetime(self, timestamp):
        if not timestamp or not isinstance(timestamp, Timestamp):
            return None
        return timestamp.ToDatetime()

    def getSongById(self, request, context):
        try:
            song, error = SongsService.findById(str(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Song not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.SongResponse(
                id=str(song.id),
                title=song.title,
                artistId=str(song.artistId),
                audioUrl=song.audioUrl,
                backgroundImage=song.backgroundImage,
                duration=song.duration,
                description=song.description,
                createdAt=self._parseTimestamp(song.createdAt),
                updatedAt=self._parseTimestamp(song.updatedAt),
                deletedAt=self._parseTimestamp(song.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getSongsByTitle(self, request, context):
        try:
            songs, error = SongsService.findByTitle(request.title)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid title")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.SongListResponse()
            for song in songs:
                songToAdd = response.songs.add()
                songToAdd.id = str(song.id)
                songToAdd.title = song.title
                songToAdd.artistId = str(song.artistId)
                songToAdd.audioUrl = song.audioUrl
                songToAdd.backgroundImage = song.backgroundImage
                songToAdd.duration = song.duration
                songToAdd.description = song.description
                songToAdd.createdAt = self._parseTimestamp(song.createdAt)
                songToAdd.updatedAt = self._parseTimestamp(song.updatedAt)
                songToAdd.deletedAt = self._parseTimestamp(song.deletedAt)
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getSongsByGenreId(self, request, context):
        try:
            songs, error = SongsService.findByGenreId(str(request.genreId))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid genre ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.SongListResponse()
            for song in songs:
                songToAdd = response.songs.add()
                songToAdd.id = str(song.id)
                songToAdd.title = song.title
                songToAdd.artistId = str(song.artistId)
                songToAdd.audioUrl = song.audioUrl
                songToAdd.backgroundImage = song.backgroundImage
                songToAdd.duration = song.duration
                songToAdd.description = song.description
                songToAdd.createdAt = self._parseTimestamp(song.createdAt)
                songToAdd.updatedAt = self._parseTimestamp(song.updatedAt)
                songToAdd.deletedAt = self._parseTimestamp(song.deletedAt)
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getSongsByAlbumId(self, request, context):
        try:
            songs, error = SongsService.findByAlbumId(str(request.albumId))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid album ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.SongListResponse()
            for song in songs:
                songToAdd = response.songs.add()
                songToAdd.id = str(song.id)
                songToAdd.title = song.title
                songToAdd.artistId = str(song.artistId)
                songToAdd.audioUrl = song.audioUrl
                songToAdd.backgroundImage = song.backgroundImage
                songToAdd.duration = song.duration
                songToAdd.description = song.description
                songToAdd.createdAt = self._parseTimestamp(song.createdAt)
                songToAdd.updatedAt = self._parseTimestamp(song.updatedAt)
                songToAdd.deletedAt = self._parseTimestamp(song.deletedAt)
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getSongsByArtistId(self, request, context):
        try:
            songs, error = SongsService.findByArtistId(str(request.artistId))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid artist ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.SongListResponse()
            for song in songs:
                songToAdd = response.songs.add()
                songToAdd.id = str(song.id)
                songToAdd.title = song.title
                songToAdd.artistId = str(song.artistId)
                songToAdd.audioUrl = song.audioUrl
                songToAdd.backgroundImage = song.backgroundImage
                songToAdd.duration = song.duration
                songToAdd.description = song.description
                songToAdd.createdAt = self._parseTimestamp(song.createdAt)
                songToAdd.updatedAt = self._parseTimestamp(song.updatedAt)
                songToAdd.deletedAt = self._parseTimestamp(song.deletedAt)
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getAllSongs(self, request, context):
        try:
            songs, error = SongsService.findAll()
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.SongListResponse()
            for song in songs:
                songToAdd = response.songs.add()
                songToAdd.id = str(song.id)
                songToAdd.title = song.title
                songToAdd.artistId = str(song.artistId)
                songToAdd.audioUrl = song.audioUrl
                songToAdd.backgroundImage = song.backgroundImage
                songToAdd.duration = song.duration
                songToAdd.description = song.description
                songToAdd.createdAt = self._parseTimestamp(song.createdAt)
                songToAdd.updatedAt = self._parseTimestamp(song.updatedAt)
                songToAdd.deletedAt = self._parseTimestamp(song.deletedAt)
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createSong(self, request, context):
        try:
            song, error = SongsService.doCreate(
                title=request.title,
                artistId=str(request.artistId),
                audioUrl=request.audioUrl,
                albumIds=request.albumIds,
                genreIds=request.genreIds,
                backgroundImage=request.backgroundImage,
                duration=request.duration,
                description=request.description,
                subArtistIds=request.subArtistIds
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Song already exists")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.SongResponse(
                id=str(song.id),
                title=song.title,
                artistId=str(song.artistId),
                audioUrl=song.audioUrl,
                backgroundImage=song.backgroundImage,
                duration=song.duration,
                description=song.description,
                createdAt=self._parseTimestamp(song.createdAt),
                updatedAt=self._parseTimestamp(song.updatedAt),
                deletedAt=self._parseTimestamp(song.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def updateSong(self, request, context):
        try:
            song, error = SongsService.doUpdate(
                id=str(request.id),
                title=request.title,
                backgroundImage=request.backgroundImage,
                duration=request.duration,
                description=request.description
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Song not found")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to update song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.SongResponse(
                id=str(song.id),
                title=song.title,
                artistId=str(song.artistId),
                audioUrl=song.audioUrl,
                backgroundImage=song.backgroundImage,
                duration=song.duration,
                description=song.description,
                createdAt=self._parseTimestamp(song.createdAt),
                updatedAt=self._parseTimestamp(song.updatedAt),
                deletedAt=self._parseTimestamp(song.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteSong(self, request, context):
        try:
            result, error = SongsService.doDelete(str(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Song not found")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.DeleteSongResponse(
                success=True,
                message="Song deleted successfully"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return musicService_pb2.DeleteSongResponse(success=False, message=str(e))

    def getAlbumById(self, request, context):
        try:
            album, error = AlbumsService.findById(str(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Album not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.AlbumResponse(
                id=str(album.id),
                name=album.name,
                description=album.description,
                backgroundImage=album.backgroundImage,
                createdAt=self._parseTimestamp(album.createdAt),
                updatedAt=self._parseTimestamp(album.updatedAt),
                deletedAt=self._parseTimestamp(album.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getAlbumsByName(self, request, context):
        try:
            albums, error = AlbumsService.findByName(request.name)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid name")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No albums found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.AlbumListResponse()
            for album in albums:
                album_proto = response.albums.add()
                album_proto.id = str(album.id)
                album_proto.name = album.name
                album_proto.description = album.description
                album_proto.backgroundImage = album.backgroundImage
                album_proto.createdAt = self._parseTimestamp(album.createdAt)
                album_proto.updatedAt = self._parseTimestamp(album.updatedAt)
                album_proto.deletedAt = self._parseTimestamp(album.deletedAt)
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getAllAlbums(self, request, context):
        try:
            albums, error = AlbumsService.findAll()
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No albums found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.AlbumListResponse()
            for album in albums:
                album_proto = response.albums.add()
                album_proto.id = str(album.id)
                album_proto.name = album.name
                album_proto.description = album.description
                album_proto.backgroundImage = album.backgroundImage
                album_proto.createdAt = self._parseTimestamp(album.createdAt)
                album_proto.updatedAt = self._parseTimestamp(album.updatedAt)
                album_proto.deletedAt = self._parseTimestamp(album.deletedAt)
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createAlbum(self, request, context):
        try:
            album, error = AlbumsService.doCreate(
                name=request.name,
                description=request.description,
                backgroundImage=request.backgroundImage
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Album already exists")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create album")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.AlbumResponse(
                id=str(album.id),
                name=album.name,
                description=album.description,
                backgroundImage=album.backgroundImage,
                createdAt=self._parseTimestamp(album.createdAt),
                updatedAt=self._parseTimestamp(album.updatedAt),
                deletedAt=self._parseTimestamp(album.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def updateAlbum(self, request, context):
        try:
            album, error = AlbumsService.doUpdate(
                id=str(request.id),
                name=request.name,
                description=request.description,
                backgroundImage=request.backgroundImage
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Album not found")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to update album")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.AlbumResponse(
                id=str(album.id),
                name=album.name,
                description=album.description,
                backgroundImage=album.backgroundImage,
                createdAt=self._parseTimestamp(album.createdAt),
                updatedAt=self._parseTimestamp(album.updatedAt),
                deletedAt=self._parseTimestamp(album.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteAlbum(self, request, context):
        try:
            result, error = AlbumsService.doDelete(str(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Album not found")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete album")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.DeleteAlbumResponse(
                success=True,
                message="Album deleted successfully"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return musicService_pb2.DeleteAlbumResponse(success=False, message=str(e))

    def getGenreById(self, request, context):
        try:
            genre, error = GenresService.findById(str(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Genre not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.GenreResponse(
                id=str(genre.id),
                name=genre.name,
                description=genre.description,
                createdAt=self._parseTimestamp(genre.createdAt),
                updatedAt=self._parseTimestamp(genre.updatedAt),
                deletedAt=self._parseTimestamp(genre.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getGenresByName(self, request, context):
        try:
            genres, error = GenresService.findByName(request.name)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid name")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No genres found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.GenreListResponse()
            for genre in genres:
                genre_proto = response.genres.add()
                genre_proto.id = str(genre.id)
                genre_proto.name = genre.name
                genre_proto.description = genre.description
                genre_proto.createdAt = self._parseTimestamp(genre.createdAt)
                genre_proto.updatedAt = self._parseTimestamp(genre.updatedAt)
                genre_proto.deletedAt = self._parseTimestamp(genre.deletedAt)
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getAllGenres(self, request, context):
        try:
            genres, error = GenresService.findAll()
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No genres found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.GenreListResponse()
            for genre in genres:
                genre_proto = response.genres.add()
                genre_proto.id = str(genre.id)
                genre_proto.name = genre.name
                genre_proto.description = genre.description
                genre_proto.createdAt = self._parseTimestamp(genre.createdAt)
                genre_proto.updatedAt = self._parseTimestamp(genre.updatedAt)
                genre_proto.deletedAt = self._parseTimestamp(genre.deletedAt)
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createGenre(self, request, context):
        try:
            genre, error = GenresService.doCreate(
                name=request.name,
                description=request.description
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Genre already exists")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create genre")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.GenreResponse(
                id=str(genre.id),
                name=genre.name,
                description=genre.description,
                createdAt=self._parseTimestamp(genre.createdAt),
                updatedAt=self._parseTimestamp(genre.updatedAt),
                deletedAt=self._parseTimestamp(genre.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def updateGenre(self, request, context):
        try:
            genre, error = GenresService.doUpdate(
                id=str(request.id),
                name=request.name,
                description=request.description
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Genre not found")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to update genre")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.GenreResponse(
                id=str(genre.id),
                name=genre.name,
                description=genre.description,
                createdAt=self._parseTimestamp(genre.createdAt),
                updatedAt=self._parseTimestamp(genre.updatedAt),
                deletedAt=self._parseTimestamp(genre.deletedAt)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteGenre(self, request, context):
        try:
            result, error = GenresService.doDelete(str(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Genre not found")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete genre")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.DeleteGenreResponse(
                success=True,
                message="Genre deleted successfully"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return musicService_pb2.DeleteGenreResponse(success=False, message=str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    musicService_pb2_grpc.add_MusicServiceServicer_to_server(MusicGrpc(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0) 