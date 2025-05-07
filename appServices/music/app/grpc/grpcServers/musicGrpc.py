import grpc
from concurrent import futures
import time
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import musicService_pb2, musicService_pb2_grpc
from app.services.songsService import SongsService
from app.services.albumsService import AlbumsService
from app.services.genresService import GenresService
from app.services.albumSongService import AlbumSongService
from app.services.genreSongService import GenreSongService
from app.services.songSubArtistService import SongSubArtistService
from common.errorCodes import ErrorCodes

class MusicGrpc(musicService_pb2_grpc.MusicServiceServicer):
    def _parseTimestamp(self, timestamp):
        if isinstance(timestamp, datetime):
            return Timestamp(seconds=int(timestamp.replace(tzinfo=None).timestamp()), nanos=timestamp.microsecond * 1000)
        elif isinstance(timestamp, (int, float)):
            return Timestamp(seconds=int(timestamp), nanos=0)
        else:
            raise ValueError("Invalid timestamp format")

    def findAllSongs(self, request, context):
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
                songProto = response.songs.add()
                songProto.id = str(song.id)
                songProto.title = song.title
                songProto.artistId = str(song.artistId)
                songProto.storageId = str(song.storageId)
                songProto.storageImageId = str(song.storageImageId) if song.storageImageId else ""
                songProto.duration = song.duration
                songProto.description = song.description
                songProto.createdAt = self._parseTimestamp(song.createdAt)
                songProto.updatedAt = self._parseTimestamp(song.updatedAt)
                songProto.deletedAt = self._parseTimestamp(song.deletedAt)
                songProto.isActive = song.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findSongById(self, request, context):
        try:
            song, error = SongsService.findById(str(request.value))
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
                song=musicService_pb2.Song(
                    id=str(song.id),
                    title=song.title,
                    artistId=str(song.artistId),
                    storageId=str(song.storageId),
                    storageImageId=str(song.storageImageId) if song.storageImageId else "",
                    duration=song.duration,
                    description=song.description,
                    createdAt=self._parseTimestamp(song.createdAt),
                    updatedAt=self._parseTimestamp(song.updatedAt),
                    deletedAt=self._parseTimestamp(song.deletedAt),
                    isActive=song.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findSongsByTitle(self, request, context):
        try:
            songs, error = SongsService.findByTitle(request.value)
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
                songProto = response.songs.add()
                songProto.id = str(song.id)
                songProto.title = song.title
                songProto.artistId = str(song.artistId)
                songProto.storageId = str(song.storageId)
                songProto.storageImageId = str(song.storageImageId) if song.storageImageId else ""
                songProto.duration = song.duration
                songProto.description = song.description
                songProto.createdAt = self._parseTimestamp(song.createdAt)
                songProto.updatedAt = self._parseTimestamp(song.updatedAt)
                songProto.deletedAt = self._parseTimestamp(song.deletedAt)
                songProto.isActive = song.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findSongsByArtistId(self, request, context):
        try:
            songs, error = SongsService.findByArtistId(str(request.value))
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
                songProto = response.songs.add()
                songProto.id = str(song.id)
                songProto.title = song.title
                songProto.artistId = str(song.artistId)
                songProto.storageId = str(song.storageId)
                songProto.storageImageId = str(song.storageImageId) if song.storageImageId else ""
                songProto.duration = song.duration
                songProto.description = song.description
                songProto.createdAt = self._parseTimestamp(song.createdAt)
                songProto.updatedAt = self._parseTimestamp(song.updatedAt)
                songProto.deletedAt = self._parseTimestamp(song.deletedAt)
                songProto.isActive = song.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createSong(self, request, context):
        try:
            song, error = SongsService.doCreate(
                title=request.title,
                artistId=request.artistId,
                storageId=request.storageId,
                albumIds=request.albumIds,
                genreIds=request.genreIds,
                storageImageId=request.storageImageId,
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
                song=musicService_pb2.Song(
                    id=str(song.id),
                    title=song.title,
                    artistId=str(song.artistId),
                    storageId=str(song.storageId),
                    storageImageId=str(song.storageImageId) if song.storageImageId else "",
                    duration=song.duration,
                    description=song.description,
                    createdAt=self._parseTimestamp(song.createdAt),
                    updatedAt=self._parseTimestamp(song.updatedAt),
                    deletedAt=self._parseTimestamp(song.deletedAt),
                    isActive=song.isActive
                )
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
                storageImageId=request.storageImageId,
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
                song=musicService_pb2.Song(
                    id=str(song.id),
                    title=song.title,
                    artistId=str(song.artistId),
                    storageId=str(song.storageId),
                    storageImageId=str(song.storageImageId) if song.storageImageId else "",
                    duration=song.duration,
                    description=song.description,
                    createdAt=self._parseTimestamp(song.createdAt),
                    updatedAt=self._parseTimestamp(song.updatedAt),
                    deletedAt=self._parseTimestamp(song.deletedAt),
                    isActive=song.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteSong(self, request, context):
        try:
            result, error = SongsService.doDelete(str(request.value))
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

            return musicService_pb2.SongResponse(
                song=musicService_pb2.Song(
                    id=str(result.id),
                    title=result.title,
                    artistId=str(result.artistId),
                    storageId=str(result.storageId),
                    storageImageId=str(result.storageImageId) if result.storageImageId else "",
                    duration=result.duration,
                    description=result.description,
                    createdAt=self._parseTimestamp(result.createdAt),
                    updatedAt=self._parseTimestamp(result.updatedAt),
                    deletedAt=self._parseTimestamp(result.deletedAt),
                    isActive=result.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findAllAlbums(self, request, context):
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
                albumProto = response.albums.add()
                albumProto.id = str(album.id)
                albumProto.name = album.name
                albumProto.description = album.description
                albumProto.storageImageId = str(album.storageImageId) if album.storageImageId else ""
                albumProto.artistId = str(album.artistId) if album.artistId else ""
                albumProto.createdAt = self._parseTimestamp(album.createdAt)
                albumProto.updatedAt = self._parseTimestamp(album.updatedAt)
                albumProto.deletedAt = self._parseTimestamp(album.deletedAt)
                albumProto.isActive = album.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findAlbumById(self, request, context):
        try:
            album, error = AlbumsService.findById(str(request.value))
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
                album=musicService_pb2.Album(
                    id=str(album.id),
                    name=album.name,
                    description=album.description,
                    storageImageId=str(album.storageImageId) if album.storageImageId else "",
                    artistId=str(album.artistId) if album.artistId else "",
                    createdAt=self._parseTimestamp(album.createdAt),
                    updatedAt=self._parseTimestamp(album.updatedAt),
                    deletedAt=self._parseTimestamp(album.deletedAt),
                    isActive=album.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findAlbumsByTitle(self, request, context):
        try:
            albums, error = AlbumsService.findByName(request.value)
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
                albumProto = response.albums.add()
                albumProto.id = str(album.id)
                albumProto.name = album.name
                albumProto.description = album.description
                albumProto.storageImageId = str(album.storageImageId) if album.storageImageId else ""
                albumProto.artistId = str(album.artistId) if album.artistId else ""
                albumProto.createdAt = self._parseTimestamp(album.createdAt)
                albumProto.updatedAt = self._parseTimestamp(album.updatedAt)
                albumProto.deletedAt = self._parseTimestamp(album.deletedAt)
                albumProto.isActive = album.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findAlbumsByArtistId(self, request, context):
        try:
            albums, error = AlbumsService.findByArtistId(str(request.value))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid artist ID")
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
                albumProto = response.albums.add()
                albumProto.id = str(album.id)
                albumProto.name = album.name
                albumProto.description = album.description
                albumProto.storageImageId = str(album.storageImageId) if album.storageImageId else ""
                albumProto.artistId = str(album.artistId) if album.artistId else ""
                albumProto.createdAt = self._parseTimestamp(album.createdAt)
                albumProto.updatedAt = self._parseTimestamp(album.updatedAt)
                albumProto.deletedAt = self._parseTimestamp(album.deletedAt)
                albumProto.isActive = album.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createAlbum(self, request, context):
        try:
            album, error = AlbumsService.doCreate(
                name=request.name,
                artistId=request.artistId,
                description=request.description,
                storageImageId=request.storageImageId
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
                album=musicService_pb2.Album(
                    id=str(album.id),
                    name=album.name,
                    description=album.description,
                    storageImageId=str(album.storageImageId) if album.storageImageId else "",
                    artistId=str(album.artistId) if album.artistId else "",
                    createdAt=self._parseTimestamp(album.createdAt),
                    updatedAt=self._parseTimestamp(album.updatedAt),
                    deletedAt=self._parseTimestamp(album.deletedAt),
                    isActive=album.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def updateAlbum(self, request, context):
        try:
            album, error = AlbumsService.doUpdate(
                id=str(request.id),
                artistId=request.artistId,
                name=request.name,
                description=request.description,
                storageImageId=request.storageImageId
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
                album=musicService_pb2.Album(
                    id=str(album.id),
                    name=album.name,
                    description=album.description,
                    storageImageId=str(album.storageImageId) if album.storageImageId else "",
                    artistId=str(album.artistId) if album.artistId else "",
                    createdAt=self._parseTimestamp(album.createdAt),
                    updatedAt=self._parseTimestamp(album.updatedAt),
                    deletedAt=self._parseTimestamp(album.deletedAt),
                    isActive=album.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteAlbum(self, request, context):
        try:
            result, error = AlbumsService.doDelete(str(request.value))
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

            return musicService_pb2.AlbumResponse(
                album=musicService_pb2.Album(
                    id=str(result.id),
                    name=result.name,
                    description=result.description,
                    storageImageId=str(result.storageImageId) if result.storageImageId else "",
                    artistId=str(result.artistId) if result.artistId else "",
                    createdAt=self._parseTimestamp(result.createdAt),
                    updatedAt=self._parseTimestamp(result.updatedAt),
                    deletedAt=self._parseTimestamp(result.deletedAt),
                    isActive=result.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findAllGenres(self, request, context):
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
                genreProto = response.genres.add()
                genreProto.id = str(genre.id)
                genreProto.name = genre.name
                genreProto.description = genre.description
                genreProto.backgroundImage = genre.backgroundImage
                genreProto.createdAt = self._parseTimestamp(genre.createdAt)
                genreProto.updatedAt = self._parseTimestamp(genre.updatedAt)
                genreProto.deletedAt = self._parseTimestamp(genre.deletedAt)
                genreProto.isActive = genre.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findGenreById(self, request, context):
        try:
            genre, error = GenresService.findById(str(request.value))
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
                genre=musicService_pb2.Genre(
                    id=str(genre.id),
                    name=genre.name,
                    description=genre.description,
                    backgroundImage=genre.backgroundImage,
                    createdAt=self._parseTimestamp(genre.createdAt),
                    updatedAt=self._parseTimestamp(genre.updatedAt),
                    deletedAt=self._parseTimestamp(genre.deletedAt),
                    isActive=genre.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findGenresByName(self, request, context):
        try:
            genres, error = GenresService.findByName(request.value)
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
                genreProto = response.genres.add()
                genreProto.id = str(genre.id)
                genreProto.name = genre.name
                genreProto.description = genre.description
                genreProto.backgroundImage = genre.backgroundImage
                genreProto.createdAt = self._parseTimestamp(genre.createdAt)
                genreProto.updatedAt = self._parseTimestamp(genre.updatedAt)
                genreProto.deletedAt = self._parseTimestamp(genre.deletedAt)
                genreProto.isActive = genre.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createGenre(self, request, context):
        try:
            genre, error = GenresService.doCreate(
                name=request.name,
                description=request.description,
                backgroundImage=request.backgroundImage,
                songIds=request.songIds
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
                genre=musicService_pb2.Genre(
                    id=str(genre.id),
                    name=genre.name,
                    description=genre.description,
                    backgroundImage=genre.backgroundImage,
                    createdAt=self._parseTimestamp(genre.createdAt),
                    updatedAt=self._parseTimestamp(genre.updatedAt),
                    deletedAt=self._parseTimestamp(genre.deletedAt),
                    isActive=genre.isActive
                )
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
                description=request.description,
                backgroundImage=request.backgroundImage
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
                genre=musicService_pb2.Genre(
                    id=str(genre.id),
                    name=genre.name,
                    description=genre.description,
                    backgroundImage=genre.backgroundImage,
                    createdAt=self._parseTimestamp(genre.createdAt),
                    updatedAt=self._parseTimestamp(genre.updatedAt),
                    deletedAt=self._parseTimestamp(genre.deletedAt),
                    isActive=genre.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteGenre(self, request, context):
        try:
            result, error = GenresService.doDelete(str(request.value))
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

            return musicService_pb2.GenreResponse(
                genre=musicService_pb2.Genre(
                    id=str(result.id),
                    name=result.name,
                    description=result.description,
                    backgroundImage=result.backgroundImage,
                    createdAt=self._parseTimestamp(result.createdAt),
                    updatedAt=self._parseTimestamp(result.updatedAt),
                    deletedAt=self._parseTimestamp(result.deletedAt),
                    isActive=result.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findAllGenreSongs(self, request, context):
        try:
            genreSongs, error = GenreSongService.findAll()
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No genre songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.GenreSongListResponse()
            for genreSong in genreSongs:
                genreSongProto = response.genreSongs.add()
                genreSongProto.genreId = str(genreSong.genreId)
                genreSongProto.songId = str(genreSong.songId)
                genreSongProto.createdAt = self._parseTimestamp(genreSong.createdAt)
                genreSongProto.updatedAt = self._parseTimestamp(genreSong.updatedAt)
                genreSongProto.deletedAt = self._parseTimestamp(genreSong.deletedAt)
                genreSongProto.isActive = genreSong.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findGenreSongByIds(self, request, context):
        try:
            genreSong, error = GenreSongService.findByIds(
                genreId=str(request.genreId),
                songId=str(request.songId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid IDs")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Genre song not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.GenreSongResponse(
                genreSong=musicService_pb2.GenreSong(
                    genreId=str(genreSong.genreId),
                    songId=str(genreSong.songId),
                    createdAt=self._parseTimestamp(genreSong.createdAt),
                    updatedAt=self._parseTimestamp(genreSong.updatedAt),
                    deletedAt=self._parseTimestamp(genreSong.deletedAt),
                    isActive=genreSong.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findGenreSongsByGenreId(self, request, context):
        try:
            genreSongs, error = GenreSongService.findByGenreId(str(request.value))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid genre ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No genre songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.GenreSongListResponse()
            for genreSong in genreSongs:
                genreSongProto = response.genreSongs.add()
                genreSongProto.genreId = str(genreSong.genreId)
                genreSongProto.songId = str(genreSong.songId)
                genreSongProto.createdAt = self._parseTimestamp(genreSong.createdAt)
                genreSongProto.updatedAt = self._parseTimestamp(genreSong.updatedAt)
                genreSongProto.deletedAt = self._parseTimestamp(genreSong.deletedAt)
                genreSongProto.isActive = genreSong.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findGenreSongsBySongId(self, request, context):
        try:
            genreSongs, error = GenreSongService.findBySongId(str(request.value))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid song ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No genre songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.GenreSongListResponse()
            for genreSong in genreSongs:
                genreSongProto = response.genreSongs.add()
                genreSongProto.genreId = str(genreSong.genreId)
                genreSongProto.songId = str(genreSong.songId)
                genreSongProto.createdAt = self._parseTimestamp(genreSong.createdAt)
                genreSongProto.updatedAt = self._parseTimestamp(genreSong.updatedAt)
                genreSongProto.deletedAt = self._parseTimestamp(genreSong.deletedAt)
                genreSongProto.isActive = genreSong.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createGenreSong(self, request, context):
        try:
            genreSong, error = GenreSongService.doCreate(
                genreId=str(request.genreId),
                songId=str(request.songId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Genre song already exists")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create genre song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.GenreSongResponse(
                genreSong=musicService_pb2.GenreSong(
                    genreId=str(genreSong.genreId),
                    songId=str(genreSong.songId),
                    createdAt=self._parseTimestamp(genreSong.createdAt),
                    updatedAt=self._parseTimestamp(genreSong.updatedAt),
                    deletedAt=self._parseTimestamp(genreSong.deletedAt),
                    isActive=genreSong.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteGenreSong(self, request, context):
        try:
            result, error = GenreSongService.doDelete(
                genreId=str(request.genreId),
                songId=str(request.songId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid IDs")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Genre song not found")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete genre song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.GenreSongResponse(
                genreSong=musicService_pb2.GenreSong(
                    genreId=str(result.genreId),
                    songId=str(result.songId),
                    createdAt=self._parseTimestamp(result.createdAt),
                    updatedAt=self._parseTimestamp(result.updatedAt),
                    deletedAt=self._parseTimestamp(result.deletedAt),
                    isActive=result.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findAllSongSubArtists(self, request, context):
        try:
            songSubArtists, error = SongSubArtistService.findAll()
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No song sub artists found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.SongSubArtistListResponse()
            for songSubArtist in songSubArtists:
                songSubArtistProto = response.songSubArtists.add()
                songSubArtistProto.songId = str(songSubArtist.songId)
                songSubArtistProto.subArtistId = str(songSubArtist.subArtistId)
                songSubArtistProto.createdAt = self._parseTimestamp(songSubArtist.createdAt)
                songSubArtistProto.updatedAt = self._parseTimestamp(songSubArtist.updatedAt)
                songSubArtistProto.deletedAt = self._parseTimestamp(songSubArtist.deletedAt)
                songSubArtistProto.isActive = songSubArtist.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findSongSubArtistByIds(self, request, context):
        try:
            songSubArtist, error = SongSubArtistService.findByIds(
                songId=str(request.songId),
                subArtistId=str(request.subArtistId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid IDs")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Song sub artist not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.SongSubArtistResponse(
                songSubArtist=musicService_pb2.SongSubArtist(
                    songId=str(songSubArtist.songId),
                    subArtistId=str(songSubArtist.subArtistId),
                    createdAt=self._parseTimestamp(songSubArtist.createdAt),
                    updatedAt=self._parseTimestamp(songSubArtist.updatedAt),
                    deletedAt=self._parseTimestamp(songSubArtist.deletedAt),
                    isActive=songSubArtist.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findSongSubArtistsBySongId(self, request, context):
        try:
            songSubArtists, error = SongSubArtistService.findBySongId(str(request.value))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid song ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No song sub artists found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.SongSubArtistListResponse()
            for songSubArtist in songSubArtists:
                songSubArtistProto = response.songSubArtists.add()
                songSubArtistProto.songId = str(songSubArtist.songId)
                songSubArtistProto.subArtistId = str(songSubArtist.subArtistId)
                songSubArtistProto.createdAt = self._parseTimestamp(songSubArtist.createdAt)
                songSubArtistProto.updatedAt = self._parseTimestamp(songSubArtist.updatedAt)
                songSubArtistProto.deletedAt = self._parseTimestamp(songSubArtist.deletedAt)
                songSubArtistProto.isActive = songSubArtist.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findSongSubArtistsBySubArtistId(self, request, context):
        try:
            songSubArtists, error = SongSubArtistService.findBySubArtistId(str(request.value))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid sub artist ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No song sub artists found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.SongSubArtistListResponse()
            for songSubArtist in songSubArtists:
                songSubArtistProto = response.songSubArtists.add()
                songSubArtistProto.songId = str(songSubArtist.songId)
                songSubArtistProto.subArtistId = str(songSubArtist.subArtistId)
                songSubArtistProto.createdAt = self._parseTimestamp(songSubArtist.createdAt)
                songSubArtistProto.updatedAt = self._parseTimestamp(songSubArtist.updatedAt)
                songSubArtistProto.deletedAt = self._parseTimestamp(songSubArtist.deletedAt)
                songSubArtistProto.isActive = songSubArtist.isActive
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createSongSubArtist(self, request, context):
        try:
            songSubArtist, error = SongSubArtistService.doCreate(
                songId=str(request.songId),
                subArtistId=str(request.subArtistId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Song sub artist already exists")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create song sub artist")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.SongSubArtistResponse(
                songSubArtist=musicService_pb2.SongSubArtist(
                    songId=str(songSubArtist.songId),
                    subArtistId=str(songSubArtist.subArtistId),
                    createdAt=self._parseTimestamp(songSubArtist.createdAt),
                    updatedAt=self._parseTimestamp(songSubArtist.updatedAt),
                    deletedAt=self._parseTimestamp(songSubArtist.deletedAt),
                    isActive=songSubArtist.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteSongSubArtist(self, request, context):
        try:
            result, error = SongSubArtistService.doDelete(
                songId=str(request.songId),
                subArtistId=str(request.subArtistId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid IDs")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Song sub artist not found")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete song sub artist")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.SongSubArtistResponse(
                songSubArtist=musicService_pb2.SongSubArtist(
                    songId=str(result.songId),
                    subArtistId=str(result.subArtistId),
                    createdAt=self._parseTimestamp(result.createdAt),
                    updatedAt=self._parseTimestamp(result.updatedAt),
                    deletedAt=self._parseTimestamp(result.deletedAt),
                    isActive=result.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteAlbumSong(self, request, context):
        try:
            result, error = AlbumSongService.doDelete(
                albumId=str(request.albumId),
                songId=str(request.songId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid IDs")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Album song not found")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete album song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.AlbumSongResponse(
                albumSong=musicService_pb2.AlbumSong(
                    albumId=str(result.albumId),
                    songId=str(result.songId),
                    createdAt=self._parseTimestamp(result.createdAt),
                    updatedAt=self._parseTimestamp(result.updatedAt),
                    deletedAt=self._parseTimestamp(result.deletedAt),
                    isActive=result.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

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
