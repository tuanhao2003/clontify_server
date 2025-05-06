import grpc
from concurrent import futures
import time
import uuid
from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import musicService_pb2, musicService_pb2_grpc
from app.services.songsService import SongsService
from app.services.albumsService import AlbumsService
from app.services.genresService import GenresService
from app.services.albumSongService import AlbumSongService
from common.errorCodes import ErrorCodes

class MusicGrpc(musicService_pb2_grpc.MusicServiceServicer):
    def GetSongById(self, request, context):
        try:
            song, error = SongsService.findById(uuid.UUID(request.id))
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
                genreId=str(song.genreId),
                audioUrl=song.audioUrl,
                backgroundImage=song.backgroundImage,
                duration=song.duration,
                createdAt=Timestamp(seconds=int(song.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(song.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(song.deletedAt.timestamp())) if song.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    # Song
    def GetSongsByTitle(self, request, context):
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

            response = musicService_pb2.SongListResponse(
                totalCount=len(songs),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for song in songs:
                song_proto = response.songs.add()
                song_proto.id = str(song.id)
                song_proto.title = song.title
                song_proto.artistId = str(song.artistId)
                song_proto.genreId = str(song.genreId)
                song_proto.audioUrl = song.audioUrl
                song_proto.backgroundImage = song.backgroundImage
                song_proto.duration = song.duration
                song_proto.createdAt = Timestamp(seconds=int(song.createdAt.timestamp()))
                song_proto.updatedAt = Timestamp(seconds=int(song.updatedAt.timestamp()))
                song_proto.deletedAt = Timestamp(seconds=int(song.deletedAt.timestamp())) if song.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def CreateSong(self, request, context):
        try:
            song, error = SongsService.create(
                title=request.title,
                artistId=uuid.UUID(request.artistId),
                genreId=uuid.UUID(request.genreId),
                audioUrl=request.audioUrl,
                backgroundImage=request.backgroundImage,
                duration=request.duration
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
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
                genreId=str(song.genreId),
                audioUrl=song.audioUrl,
                backgroundImage=song.backgroundImage,
                duration=song.duration,
                createdAt=Timestamp(seconds=int(song.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(song.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(song.deletedAt.timestamp())) if song.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def UpdateSong(self, request, context):
        try:
            song, error = SongsService.update(
                id=uuid.UUID(request.id),
                title=request.title,
                artistId=uuid.UUID(request.artistId),
                genreId=uuid.UUID(request.genreId),
                audioUrl=request.audioUrl,
                backgroundImage=request.backgroundImage,
                duration=request.duration
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
                genreId=str(song.genreId),
                audioUrl=song.audioUrl,
                backgroundImage=song.backgroundImage,
                duration=song.duration,
                createdAt=Timestamp(seconds=int(song.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(song.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(song.deletedAt.timestamp())) if song.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def DeleteSong(self, request, context):
        try:
            result, error = SongsService.delete(uuid.UUID(request.id))
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

    def GetAlbumById(self, request, context):
        try:
            album, error = AlbumsService.findById(uuid.UUID(request.id))
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
                createdAt=Timestamp(seconds=int(album.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(album.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(album.deletedAt.timestamp())) if album.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def GetAlbumsByName(self, request, context):
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

            response = musicService_pb2.AlbumListResponse(
                totalCount=len(albums),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for album in albums:
                album_proto = response.albums.add()
                album_proto.id = str(album.id)
                album_proto.name = album.name
                album_proto.description = album.description
                album_proto.backgroundImage = album.backgroundImage
                album_proto.createdAt = Timestamp(seconds=int(album.createdAt.timestamp()))
                album_proto.updatedAt = Timestamp(seconds=int(album.updatedAt.timestamp()))
                album_proto.deletedAt = Timestamp(seconds=int(album.deletedAt.timestamp())) if album.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def CreateAlbum(self, request, context):
        try:
            album, error = AlbumsService.create(
                name=request.name,
                description=request.description,
                backgroundImage=request.backgroundImage
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
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
                createdAt=Timestamp(seconds=int(album.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(album.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(album.deletedAt.timestamp())) if album.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def UpdateAlbum(self, request, context):
        try:
            album, error = AlbumsService.update(
                id=uuid.UUID(request.id),
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
                createdAt=Timestamp(seconds=int(album.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(album.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(album.deletedAt.timestamp())) if album.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def DeleteAlbum(self, request, context):
        try:
            result, error = AlbumsService.delete(uuid.UUID(request.id))
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

    def GetGenreById(self, request, context):
        try:
            genre, error = GenresService.findById(uuid.UUID(request.id))
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
                createdAt=Timestamp(seconds=int(genre.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(genre.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(genre.deletedAt.timestamp())) if genre.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def GetGenresByName(self, request, context):
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

            response = musicService_pb2.GenreListResponse(
                totalCount=len(genres),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for genre in genres:
                genre_proto = response.genres.add()
                genre_proto.id = str(genre.id)
                genre_proto.name = genre.name
                genre_proto.description = genre.description
                genre_proto.createdAt = Timestamp(seconds=int(genre.createdAt.timestamp()))
                genre_proto.updatedAt = Timestamp(seconds=int(genre.updatedAt.timestamp()))
                genre_proto.deletedAt = Timestamp(seconds=int(genre.deletedAt.timestamp())) if genre.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def CreateGenre(self, request, context):
        try:
            genre, error = GenresService.create(
                name=request.name,
                description=request.description
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
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
                createdAt=Timestamp(seconds=int(genre.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(genre.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(genre.deletedAt.timestamp())) if genre.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def UpdateGenre(self, request, context):
        try:
            genre, error = GenresService.update(
                id=uuid.UUID(request.id),
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
                createdAt=Timestamp(seconds=int(genre.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(genre.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(genre.deletedAt.timestamp())) if genre.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def DeleteGenre(self, request, context):
        try:
            result, error = GenresService.delete(uuid.UUID(request.id))
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