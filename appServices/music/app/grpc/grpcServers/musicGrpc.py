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
    def _parseTimestamp(self, dt):
        if not dt or not isinstance(dt, datetime):
            return None
        timestamp = Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp

    def filterAllSongs(self, request, context):
        try:
            songs, error = SongsService.findAll()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for song in songs:
                yield musicService_pb2.Song(
                    id=str(song.id),
                    title=song.title,
                    artistId=str(song.artistId),
                    storageId=str(song.storageId),
                    storageImageId=str(song.storageImageId) if song.storageImageId else "",
                    duration=song.duration,
                    description=song.description,
                    songType=song.songType,
                    createdAt=self._parseTimestamp(song.createdAt),
                    updatedAt=self._parseTimestamp(song.updatedAt),
                    deletedAt=self._parseTimestamp(song.deletedAt),
                    isActive=song.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getSongById(self, request, context):
        try:
            song, error = SongsService.findById(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Song(
                id=str(song.id),
                title=song.title,
                artistId=str(song.artistId),
                storageId=str(song.storageId),
                storageImageId=str(song.storageImageId) if song.storageImageId else "",
                duration=song.duration,
                description=song.description,
                songType=song.songType,
                createdAt=self._parseTimestamp(song.createdAt),
                updatedAt=self._parseTimestamp(song.updatedAt),
                deletedAt=self._parseTimestamp(song.deletedAt),
                isActive=song.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterSongsByTitle(self, request, context):
        try:
            songs, error = SongsService.findByTitle(request.value)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for song in songs:
                yield musicService_pb2.Song(
                    id=str(song.id),
                    title=song.title,
                    artistId=str(song.artistId),
                    storageId=str(song.storageId),
                    storageImageId=str(song.storageImageId) if song.storageImageId else "",
                    duration=song.duration,
                    description=song.description,
                    songType=song.songType,
                    createdAt=self._parseTimestamp(song.createdAt),
                    updatedAt=self._parseTimestamp(song.updatedAt),
                    deletedAt=self._parseTimestamp(song.deletedAt),
                    isActive=song.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterSongsByArtistId(self, request, context):
        try:
            songs, error = SongsService.findByArtistId(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for song in songs:
                yield musicService_pb2.Song(
                    id=str(song.id),
                    title=song.title,
                    artistId=str(song.artistId),
                    storageId=str(song.storageId),
                    storageImageId=str(song.storageImageId) if song.storageImageId else "",
                    duration=song.duration,
                    description=song.description,
                    songType=song.songType,
                    createdAt=self._parseTimestamp(song.createdAt),
                    updatedAt=self._parseTimestamp(song.updatedAt),
                    deletedAt=self._parseTimestamp(song.deletedAt),
                    isActive=song.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterSongsBySongType(self, request, context):
        try:
            songs, error = SongsService.findBySongType(request.value)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for song in songs:
                yield musicService_pb2.Song(
                    id=str(song.id),
                    title=song.title,
                    artistId=str(song.artistId),
                    storageId=str(song.storageId),
                    storageImageId=str(song.storageImageId) if song.storageImageId else "",
                    duration=song.duration,
                    description=song.description,
                    songType=song.songType,
                    createdAt=self._parseTimestamp(song.createdAt),
                    updatedAt=self._parseTimestamp(song.updatedAt),
                    deletedAt=self._parseTimestamp(song.deletedAt),
                    isActive=song.isActive
                )
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
                storageImageId=request.storageImageId,
                duration=request.duration,
                description=request.description,
                songType=request.songType
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Song(
                id=str(song.id),
                title=song.title,
                artistId=str(song.artistId),
                storageId=str(song.storageId),
                storageImageId=str(song.storageImageId) if song.storageImageId else "",
                duration=song.duration,
                description=song.description,
                songType=song.songType,
                createdAt=self._parseTimestamp(song.createdAt),
                updatedAt=self._parseTimestamp(song.updatedAt),
                deletedAt=self._parseTimestamp(song.deletedAt),
                isActive=song.isActive
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
                description=request.description,
                songType=request.songType
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Song(
                id=str(song.id),
                title=song.title,
                artistId=str(song.artistId),
                storageId=str(song.storageId),
                storageImageId=str(song.storageImageId) if song.storageImageId else "",
                duration=song.duration,
                description=song.description,
                songType=song.songType,
                createdAt=self._parseTimestamp(song.createdAt),
                updatedAt=self._parseTimestamp(song.updatedAt),
                deletedAt=self._parseTimestamp(song.deletedAt),
                isActive=song.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteSong(self, request, context):
        try:
            song, error = SongsService.doDelete(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Song(
                id=str(song.id),
                title=song.title,
                artistId=str(song.artistId),
                storageId=str(song.storageId),
                storageImageId=str(song.storageImageId) if song.storageImageId else "",
                duration=song.duration,
                description=song.description,
                songType=song.songType,
                createdAt=self._parseTimestamp(song.createdAt),
                updatedAt=self._parseTimestamp(song.updatedAt),
                deletedAt=self._parseTimestamp(song.deletedAt),
                isActive=song.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterAllAlbums(self, request, context):
        try:
            albums, error = AlbumsService.findAll()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for album in albums:
                yield musicService_pb2.Album(
                    id=str(album.id),
                    name=album.name,
                    description=album.description,
                    storageImageId=str(album.storageImageId) if album.storageImageId else "",
                    artistId=str(album.artistId),
                    createdAt=self._parseTimestamp(album.createdAt),
                    updatedAt=self._parseTimestamp(album.updatedAt),
                    deletedAt=self._parseTimestamp(album.deletedAt),
                    isActive=album.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getAlbumById(self, request, context):
        try:
            album, error = AlbumsService.findById(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Album(
                id=str(album.id),
                name=album.name,
                description=album.description,
                storageImageId=str(album.storageImageId) if album.storageImageId else "",
                artistId=str(album.artistId),
                createdAt=self._parseTimestamp(album.createdAt),
                updatedAt=self._parseTimestamp(album.updatedAt),
                deletedAt=self._parseTimestamp(album.deletedAt),
                isActive=album.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterAlbumsByName(self, request, context):
        try:
            albums, error = AlbumsService.findByName(request.value)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for album in albums:
                yield musicService_pb2.Album(
                    id=str(album.id),
                    name=album.name,
                    description=album.description,
                    storageImageId=str(album.storageImageId) if album.storageImageId else "",
                    artistId=str(album.artistId),
                    createdAt=self._parseTimestamp(album.createdAt),
                    updatedAt=self._parseTimestamp(album.updatedAt),
                    deletedAt=self._parseTimestamp(album.deletedAt),
                    isActive=album.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterAlbumsByArtistId(self, request, context):
        try:
            albums, error = AlbumsService.findByArtistId(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for album in albums:
                yield musicService_pb2.Album(
                    id=str(album.id),
                    name=album.name,
                    description=album.description,
                    storageImageId=str(album.storageImageId) if album.storageImageId else "",
                    artistId=str(album.artistId),
                    createdAt=self._parseTimestamp(album.createdAt),
                    updatedAt=self._parseTimestamp(album.updatedAt),
                    deletedAt=self._parseTimestamp(album.deletedAt),
                    isActive=album.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createAlbum(self, request, context):
        try:
            album, error = AlbumsService.doCreate(
                name=request.name,
                description=request.description,
                storageImageId=request.storageImageId,
                artistId=request.artistId
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Album(
                id=str(album.id),
                name=album.name,
                description=album.description,
                storageImageId=str(album.storageImageId) if album.storageImageId else "",
                artistId=str(album.artistId),
                createdAt=self._parseTimestamp(album.createdAt),
                updatedAt=self._parseTimestamp(album.updatedAt),
                deletedAt=self._parseTimestamp(album.deletedAt),
                isActive=album.isActive
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
                storageImageId=request.storageImageId,
                artistId=request.artistId
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Album(
                id=str(album.id),
                name=album.name,
                description=album.description,
                storageImageId=str(album.storageImageId) if album.storageImageId else "",
                artistId=str(album.artistId),
                createdAt=self._parseTimestamp(album.createdAt),
                updatedAt=self._parseTimestamp(album.updatedAt),
                deletedAt=self._parseTimestamp(album.deletedAt),
                isActive=album.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteAlbum(self, request, context):
        try:
            album, error = AlbumsService.doDelete(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Album(
                id=str(album.id),
                name=album.name,
                description=album.description,
                storageImageId=str(album.storageImageId) if album.storageImageId else "",
                artistId=str(album.artistId),
                createdAt=self._parseTimestamp(album.createdAt),
                updatedAt=self._parseTimestamp(album.updatedAt),
                deletedAt=self._parseTimestamp(album.deletedAt),
                isActive=album.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterAllGenres(self, request, context):
        try:
            genres, error = GenresService.findAll()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for genre in genres:
                yield musicService_pb2.Genre(
                    id=str(genre.id),
                    name=genre.name,
                    description=genre.description,
                    backgroundImage=genre.backgroundImage,
                    createdAt=self._parseTimestamp(genre.createdAt),
                    updatedAt=self._parseTimestamp(genre.updatedAt),
                    deletedAt=self._parseTimestamp(genre.deletedAt),
                    isActive=genre.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getGenreById(self, request, context):
        try:
            genre, error = GenresService.findById(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Genre(
                id=str(genre.id),
                name=genre.name,
                description=genre.description,
                backgroundImage=genre.backgroundImage,
                createdAt=self._parseTimestamp(genre.createdAt),
                updatedAt=self._parseTimestamp(genre.updatedAt),
                deletedAt=self._parseTimestamp(genre.deletedAt),
                isActive=genre.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterGenresByName(self, request, context):
        try:
            genres, error = GenresService.findByName(request.value)
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for genre in genres:
                yield musicService_pb2.Genre(
                    id=str(genre.id),
                    name=genre.name,
                    description=genre.description,
                    backgroundImage=genre.backgroundImage,
                    createdAt=self._parseTimestamp(genre.createdAt),
                    updatedAt=self._parseTimestamp(genre.updatedAt),
                    deletedAt=self._parseTimestamp(genre.deletedAt),
                    isActive=genre.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createGenre(self, request, context):
        try:
            genre, error = GenresService.doCreate(
                name=request.name,
                description=request.description,
                backgroundImage=request.backgroundImage
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Genre(
                id=str(genre.id),
                name=genre.name,
                description=genre.description,
                backgroundImage=genre.backgroundImage,
                createdAt=self._parseTimestamp(genre.createdAt),
                updatedAt=self._parseTimestamp(genre.updatedAt),
                deletedAt=self._parseTimestamp(genre.deletedAt),
                isActive=genre.isActive
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
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Genre(
                id=str(genre.id),
                name=genre.name,
                description=genre.description,
                backgroundImage=genre.backgroundImage,
                createdAt=self._parseTimestamp(genre.createdAt),
                updatedAt=self._parseTimestamp(genre.updatedAt),
                deletedAt=self._parseTimestamp(genre.deletedAt),
                isActive=genre.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteGenre(self, request, context):
        try:
            genre, error = GenresService.doDelete(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.Genre(
                id=str(genre.id),
                name=genre.name,
                description=genre.description,
                backgroundImage=genre.backgroundImage,
                createdAt=self._parseTimestamp(genre.createdAt),
                updatedAt=self._parseTimestamp(genre.updatedAt),
                deletedAt=self._parseTimestamp(genre.deletedAt),
                isActive=genre.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterAllAlbumSongs(self, request, context):
        try:
            albumSongs, error = AlbumSongService.findAll()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for albumSong in albumSongs:
                yield musicService_pb2.AlbumSong(
                    albumId=str(albumSong.albumId),
                    songId=str(albumSong.songId),
                    createdAt=self._parseTimestamp(albumSong.createdAt),
                    updatedAt=self._parseTimestamp(albumSong.updatedAt),
                    deletedAt=self._parseTimestamp(albumSong.deletedAt),
                    isActive=albumSong.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getAlbumSongByIds(self, request, context):
        try:
            albumSong, error = AlbumSongService.findByIds(
                albumId=str(request.albumId),
                songId=str(request.songId)
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.AlbumSong(
                albumId=str(albumSong.albumId),
                songId=str(albumSong.songId),
                createdAt=self._parseTimestamp(albumSong.createdAt),
                updatedAt=self._parseTimestamp(albumSong.updatedAt),
                deletedAt=self._parseTimestamp(albumSong.deletedAt),
                isActive=albumSong.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterAlbumSongsByAlbumId(self, request, context):
        try:
            albumSongs, error = AlbumSongService.findByAlbumId(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for albumSong in albumSongs:
                yield musicService_pb2.AlbumSong(
                    albumId=str(albumSong.albumId),
                    songId=str(albumSong.songId),
                    createdAt=self._parseTimestamp(albumSong.createdAt),
                    updatedAt=self._parseTimestamp(albumSong.updatedAt),
                    deletedAt=self._parseTimestamp(albumSong.deletedAt),
                    isActive=albumSong.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterAlbumSongsBySongId(self, request, context):
        try:
            albumSongs, error = AlbumSongService.findBySongId(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for albumSong in albumSongs:
                yield musicService_pb2.AlbumSong(
                    albumId=str(albumSong.albumId),
                    songId=str(albumSong.songId),
                    createdAt=self._parseTimestamp(albumSong.createdAt),
                    updatedAt=self._parseTimestamp(albumSong.updatedAt),
                    deletedAt=self._parseTimestamp(albumSong.deletedAt),
                    isActive=albumSong.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def createAlbumSong(self, request, context):
        try:
            albumSong, error = AlbumSongService.doCreate(
                albumId=str(request.albumId),
                songId=str(request.songId)
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.AlbumSong(
                albumId=str(albumSong.albumId),
                songId=str(albumSong.songId),
                createdAt=self._parseTimestamp(albumSong.createdAt),
                updatedAt=self._parseTimestamp(albumSong.updatedAt),
                deletedAt=self._parseTimestamp(albumSong.deletedAt),
                isActive=albumSong.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteAlbumSong(self, request, context):
        try:
            albumSong, error = AlbumSongService.doDelete(
                albumId=str(request.albumId),
                songId=str(request.songId)
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.AlbumSong(
                albumId=str(albumSong.albumId),
                songId=str(albumSong.songId),
                createdAt=self._parseTimestamp(albumSong.createdAt),
                updatedAt=self._parseTimestamp(albumSong.updatedAt),
                deletedAt=self._parseTimestamp(albumSong.deletedAt),
                isActive=albumSong.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterAllGenreSongs(self, request, context):
        try:
            genreSongs, error = GenreSongService.findAll()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for genreSong in genreSongs:
                yield musicService_pb2.GenreSong(
                    genreId=str(genreSong.genreId),
                    songId=str(genreSong.songId),
                    createdAt=self._parseTimestamp(genreSong.createdAt),
                    updatedAt=self._parseTimestamp(genreSong.updatedAt),
                    deletedAt=self._parseTimestamp(genreSong.deletedAt),
                    isActive=genreSong.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getGenreSongByIds(self, request, context):
        try:
            genreSong, error = GenreSongService.findByIds(
                genreId=str(request.genreId),
                songId=str(request.songId)
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.GenreSong(
                genreId=str(genreSong.genreId),
                songId=str(genreSong.songId),
                createdAt=self._parseTimestamp(genreSong.createdAt),
                updatedAt=self._parseTimestamp(genreSong.updatedAt),
                deletedAt=self._parseTimestamp(genreSong.deletedAt),
                isActive=genreSong.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterGenreSongsByGenreId(self, request, context):
        try:
            genreSongs, error = GenreSongService.findByGenreId(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for genreSong in genreSongs:
                yield musicService_pb2.GenreSong(
                    genreId=str(genreSong.genreId),
                    songId=str(genreSong.songId),
                    createdAt=self._parseTimestamp(genreSong.createdAt),
                    updatedAt=self._parseTimestamp(genreSong.updatedAt),
                    deletedAt=self._parseTimestamp(genreSong.deletedAt),
                    isActive=genreSong.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterGenreSongsBySongId(self, request, context):
        try:
            genreSongs, error = GenreSongService.findBySongId(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for genreSong in genreSongs:
                yield musicService_pb2.GenreSong(
                    genreId=str(genreSong.genreId),
                    songId=str(genreSong.songId),
                    createdAt=self._parseTimestamp(genreSong.createdAt),
                    updatedAt=self._parseTimestamp(genreSong.updatedAt),
                    deletedAt=self._parseTimestamp(genreSong.deletedAt),
                    isActive=genreSong.isActive
                )
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
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.GenreSong(
                genreId=str(genreSong.genreId),
                songId=str(genreSong.songId),
                createdAt=self._parseTimestamp(genreSong.createdAt),
                updatedAt=self._parseTimestamp(genreSong.updatedAt),
                deletedAt=self._parseTimestamp(genreSong.deletedAt),
                isActive=genreSong.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteGenreSong(self, request, context):
        try:
            genreSong, error = GenreSongService.doDelete(
                genreId=str(request.genreId),
                songId=str(request.songId)
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.GenreSong(
                genreId=str(genreSong.genreId),
                songId=str(genreSong.songId),
                createdAt=self._parseTimestamp(genreSong.createdAt),
                updatedAt=self._parseTimestamp(genreSong.updatedAt),
                deletedAt=self._parseTimestamp(genreSong.deletedAt),
                isActive=genreSong.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterAllSongSubArtists(self, request, context):
        try:
            songSubArtists, error = SongSubArtistService.findAll()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for songSubArtist in songSubArtists:
                yield musicService_pb2.SongSubArtist(
                    songId=str(songSubArtist.songId),
                    subArtistId=str(songSubArtist.subArtistId),
                    createdAt=self._parseTimestamp(songSubArtist.createdAt),
                    updatedAt=self._parseTimestamp(songSubArtist.updatedAt),
                    deletedAt=self._parseTimestamp(songSubArtist.deletedAt),
                    isActive=songSubArtist.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def getSongSubArtistByIds(self, request, context):
        try:
            songSubArtist, error = SongSubArtistService.findByIds(
                songId=str(request.songId),
                subArtistId=str(request.subArtistId)
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.SongSubArtist(
                songId=str(songSubArtist.songId),
                subArtistId=str(songSubArtist.subArtistId),
                createdAt=self._parseTimestamp(songSubArtist.createdAt),
                updatedAt=self._parseTimestamp(songSubArtist.updatedAt),
                deletedAt=self._parseTimestamp(songSubArtist.deletedAt),
                isActive=songSubArtist.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterSongSubArtistsBySongId(self, request, context):
        try:
            songSubArtists, error = SongSubArtistService.findBySongId(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for songSubArtist in songSubArtists:
                yield musicService_pb2.SongSubArtist(
                    songId=str(songSubArtist.songId),
                    subArtistId=str(songSubArtist.subArtistId),
                    createdAt=self._parseTimestamp(songSubArtist.createdAt),
                    updatedAt=self._parseTimestamp(songSubArtist.updatedAt),
                    deletedAt=self._parseTimestamp(songSubArtist.deletedAt),
                    isActive=songSubArtist.isActive
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def filterSongSubArtistsBySubArtistId(self, request, context):
        try:
            songSubArtists, error = SongSubArtistService.findBySubArtistId(str(request.value))
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            for songSubArtist in songSubArtists:
                yield musicService_pb2.SongSubArtist(
                    songId=str(songSubArtist.songId),
                    subArtistId=str(songSubArtist.subArtistId),
                    createdAt=self._parseTimestamp(songSubArtist.createdAt),
                    updatedAt=self._parseTimestamp(songSubArtist.updatedAt),
                    deletedAt=self._parseTimestamp(songSubArtist.deletedAt),
                    isActive=songSubArtist.isActive
                )
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
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.SongSubArtist(
                songId=str(songSubArtist.songId),
                subArtistId=str(songSubArtist.subArtistId),
                createdAt=self._parseTimestamp(songSubArtist.createdAt),
                updatedAt=self._parseTimestamp(songSubArtist.updatedAt),
                deletedAt=self._parseTimestamp(songSubArtist.deletedAt),
                isActive=songSubArtist.isActive
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def deleteSongSubArtist(self, request, context):
        try:
            songSubArtist, error = SongSubArtistService.doDelete(
                songId=str(request.songId),
                subArtistId=str(request.subArtistId)
            )
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(error))
                return None
            return musicService_pb2.SongSubArtist(
                songId=str(songSubArtist.songId),
                subArtistId=str(songSubArtist.subArtistId),
                createdAt=self._parseTimestamp(songSubArtist.createdAt),
                updatedAt=self._parseTimestamp(songSubArtist.updatedAt),
                deletedAt=self._parseTimestamp(songSubArtist.deletedAt),
                isActive=songSubArtist.isActive
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
