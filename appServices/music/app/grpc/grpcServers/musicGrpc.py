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
from app.services.playlistsService import PlaylistsService
from app.services.albumSongService import AlbumSongService
from app.services.playlistSongService import PlaylistSongService
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

    # Album
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

    # Genre
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

    # Playlist
    def GetPlaylistById(self, request, context):
        try:
            playlist, error = PlaylistsService.findById(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Playlist not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.PlaylistResponse(
                id=str(playlist.id),
                name=playlist.name,
                description=playlist.description,
                ownerId=str(playlist.ownerId),
                isPublic=playlist.isPublic,
                createdAt=Timestamp(seconds=int(playlist.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(playlist.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(playlist.deletedAt.timestamp())) if playlist.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def GetPlaylistsByName(self, request, context):
        try:
            playlists, error = PlaylistsService.findByName(request.name)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid name")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No playlists found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.PlaylistListResponse(
                totalCount=len(playlists),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for playlist in playlists:
                playlist_proto = response.playlists.add()
                playlist_proto.id = str(playlist.id)
                playlist_proto.name = playlist.name
                playlist_proto.description = playlist.description
                playlist_proto.ownerId = str(playlist.ownerId)
                playlist_proto.isPublic = playlist.isPublic
                playlist_proto.createdAt = Timestamp(seconds=int(playlist.createdAt.timestamp()))
                playlist_proto.updatedAt = Timestamp(seconds=int(playlist.updatedAt.timestamp()))
                playlist_proto.deletedAt = Timestamp(seconds=int(playlist.deletedAt.timestamp())) if playlist.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def GetPlaylistsByOwnerId(self, request, context):
        try:
            playlists, error = PlaylistsService.findByOwnerId(uuid.UUID(request.ownerId))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid owner ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No playlists found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.PlaylistListResponse(
                totalCount=len(playlists),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for playlist in playlists:
                playlist_proto = response.playlists.add()
                playlist_proto.id = str(playlist.id)
                playlist_proto.name = playlist.name
                playlist_proto.description = playlist.description
                playlist_proto.ownerId = str(playlist.ownerId)
                playlist_proto.isPublic = playlist.isPublic
                playlist_proto.createdAt = Timestamp(seconds=int(playlist.createdAt.timestamp()))
                playlist_proto.updatedAt = Timestamp(seconds=int(playlist.updatedAt.timestamp()))
                playlist_proto.deletedAt = Timestamp(seconds=int(playlist.deletedAt.timestamp())) if playlist.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def CreatePlaylist(self, request, context):
        try:
            playlist, error = PlaylistsService.create(
                name=request.name,
                description=request.description,
                ownerId=uuid.UUID(request.ownerId),
                isPublic=request.isPublic
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create playlist")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.PlaylistResponse(
                id=str(playlist.id),
                name=playlist.name,
                description=playlist.description,
                ownerId=str(playlist.ownerId),
                isPublic=playlist.isPublic,
                createdAt=Timestamp(seconds=int(playlist.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(playlist.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(playlist.deletedAt.timestamp())) if playlist.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def UpdatePlaylist(self, request, context):
        try:
            playlist, error = PlaylistsService.update(
                id=uuid.UUID(request.id),
                name=request.name,
                description=request.description,
                ownerId=uuid.UUID(request.ownerId),
                isPublic=request.isPublic
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Playlist not found")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to update playlist")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.PlaylistResponse(
                id=str(playlist.id),
                name=playlist.name,
                description=playlist.description,
                ownerId=str(playlist.ownerId),
                isPublic=playlist.isPublic,
                createdAt=Timestamp(seconds=int(playlist.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(playlist.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(playlist.deletedAt.timestamp())) if playlist.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def DeletePlaylist(self, request, context):
        try:
            result, error = PlaylistsService.delete(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Playlist not found")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete playlist")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.DeletePlaylistResponse(
                success=True,
                message="Playlist deleted successfully"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return musicService_pb2.DeletePlaylistResponse(success=False, message=str(e))

    # AlbumSong
    def GetAlbumSongById(self, request, context):
        try:
            albumSong, error = AlbumSongService.findById(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("AlbumSong not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.AlbumSongResponse(
                id=str(albumSong.id),
                albumId=str(albumSong.albumId),
                songId=str(albumSong.songId),
                createdAt=Timestamp(seconds=int(albumSong.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(albumSong.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(albumSong.deletedAt.timestamp())) if albumSong.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def GetAlbumSongsByAlbumId(self, request, context):
        try:
            albumSongs, error = AlbumSongService.findByAlbumId(uuid.UUID(request.albumId))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid album ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No album songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.AlbumSongListResponse(
                totalCount=len(albumSongs),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for albumSong in albumSongs:
                albumSong_proto = response.albumSongs.add()
                albumSong_proto.id = str(albumSong.id)
                albumSong_proto.albumId = str(albumSong.albumId)
                albumSong_proto.songId = str(albumSong.songId)
                albumSong_proto.createdAt = Timestamp(seconds=int(albumSong.createdAt.timestamp()))
                albumSong_proto.updatedAt = Timestamp(seconds=int(albumSong.updatedAt.timestamp()))
                albumSong_proto.deletedAt = Timestamp(seconds=int(albumSong.deletedAt.timestamp())) if albumSong.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def GetAlbumSongsBySongId(self, request, context):
        try:
            albumSongs, error = AlbumSongService.findBySongId(uuid.UUID(request.songId))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid song ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No album songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.AlbumSongListResponse(
                totalCount=len(albumSongs),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for albumSong in albumSongs:
                albumSong_proto = response.albumSongs.add()
                albumSong_proto.id = str(albumSong.id)
                albumSong_proto.albumId = str(albumSong.albumId)
                albumSong_proto.songId = str(albumSong.songId)
                albumSong_proto.createdAt = Timestamp(seconds=int(albumSong.createdAt.timestamp()))
                albumSong_proto.updatedAt = Timestamp(seconds=int(albumSong.updatedAt.timestamp()))
                albumSong_proto.deletedAt = Timestamp(seconds=int(albumSong.deletedAt.timestamp())) if albumSong.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def GetPlaylistSongsByPlaylistId(self, request, context):
        try:
            playlistSongs, error = PlaylistSongService.findByPlaylistId(uuid.UUID(request.playlistId))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid playlist ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No playlist songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.PlaylistSongListResponse(
                totalCount=len(playlistSongs),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for playlistSong in playlistSongs:
                playlistSong_proto = response.playlistSongs.add()
                playlistSong_proto.id = str(playlistSong.id)
                playlistSong_proto.playlistId = str(playlistSong.playlistId)
                playlistSong_proto.songId = str(playlistSong.songId)
                playlistSong_proto.createdAt = Timestamp(seconds=int(playlistSong.createdAt.timestamp()))
                playlistSong_proto.updatedAt = Timestamp(seconds=int(playlistSong.updatedAt.timestamp()))
                playlistSong_proto.deletedAt = Timestamp(seconds=int(playlistSong.deletedAt.timestamp())) if playlistSong.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def GetPlaylistSongsBySongId(self, request, context):
        try:
            playlistSongs, error = PlaylistSongService.findBySongId(uuid.UUID(request.songId))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid song ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No playlist songs found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = musicService_pb2.PlaylistSongListResponse(
                totalCount=len(playlistSongs),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for playlistSong in playlistSongs:
                playlistSong_proto = response.playlistSongs.add()
                playlistSong_proto.id = str(playlistSong.id)
                playlistSong_proto.playlistId = str(playlistSong.playlistId)
                playlistSong_proto.songId = str(playlistSong.songId)
                playlistSong_proto.createdAt = Timestamp(seconds=int(playlistSong.createdAt.timestamp()))
                playlistSong_proto.updatedAt = Timestamp(seconds=int(playlistSong.updatedAt.timestamp()))
                playlistSong_proto.deletedAt = Timestamp(seconds=int(playlistSong.deletedAt.timestamp())) if playlistSong.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def CreatePlaylistSong(self, request, context):
        pass
    def UpdatePlaylistSong(self, request, context):
        try:
            playlistSong, error = PlaylistSongService.update(
                id=uuid.UUID(request.id),
                playlistId=uuid.UUID(request.playlistId),
                songId=uuid.UUID(request.songId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Playlist song not found")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to update playlist song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.PlaylistSongResponse(
                id=str(playlistSong.id),
                playlistId=str(playlistSong.playlistId),
                songId=str(playlistSong.songId),
                createdAt=Timestamp(seconds=int(playlistSong.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(playlistSong.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(playlistSong.deletedAt.timestamp())) if playlistSong.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
    def DeletePlaylistSong(self, request, context):
        try:
            result, error = PlaylistSongService.delete(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Playlist song not found")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete playlist song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.DeletePlaylistSongResponse(
                success=True,
                message="Playlist song deleted successfully"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return musicService_pb2.DeletePlaylistSongResponse(success=False, message=str(e))

    def CreateAlbumSong(self, request, context):
        try:
            albumSong, error = AlbumSongService.create(
                albumId=uuid.UUID(request.albumId),
                songId=uuid.UUID(request.songId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create album song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.AlbumSongResponse(
                id=str(albumSong.id),
                albumId=str(albumSong.albumId),
                songId=str(albumSong.songId),
                createdAt=Timestamp(seconds=int(albumSong.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(albumSong.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(albumSong.deletedAt.timestamp())) if albumSong.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def UpdateAlbumSong(self, request, context):
        try:
            albumSong, error = AlbumSongService.update(
                id=uuid.UUID(request.id),
                albumId=uuid.UUID(request.albumId),
                songId=uuid.UUID(request.songId)
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Album song not found")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to update album song")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return musicService_pb2.AlbumSongResponse(
                id=str(albumSong.id),
                albumId=str(albumSong.albumId),
                songId=str(albumSong.songId),
                createdAt=Timestamp(seconds=int(albumSong.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(albumSong.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(albumSong.deletedAt.timestamp())) if albumSong.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def DeleteAlbumSong(self, request, context):
        try:
            result, error = AlbumSongService.delete(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
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

            return musicService_pb2.DeleteAlbumSongResponse(
                success=True,
                message="Album song deleted successfully"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return musicService_pb2.DeleteAlbumSongResponse(success=False, message=str(e))

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