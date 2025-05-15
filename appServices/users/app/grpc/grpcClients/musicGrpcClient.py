import grpc
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import musicService_pb2
from app.grpc.protos import musicService_pb2_grpc
from google.protobuf import empty_pb2
from django.conf import settings
from common.errorCodes import ErrorCodes

class MusicGrpcClient:
    def __init__(self):
        self.host = getattr(settings, 'MUSIC_GRPC_HOST', 'music_service')
        self.port = getattr(settings, 'MUSIC_GRPC_PORT', '50053')
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = musicService_pb2_grpc.MusicServiceStub(self.channel)
    
    def close(self):
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None
    
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
    
    def _songSerializer(self, song):
        return {
            'id': song.id,
            'title': song.title,
            'artistID': song.artistID,
            'storageID': song.storageID,
            'storageImageID': song.storageImageID,
            'duration': song.duration,
            'description': song.description,
            'songType': song.songType,
            'createdAt': self._parseDatetime(song.createdAt),
            'updatedAt': self._parseDatetime(song.updatedAt),
            'deletedAt': self._parseDatetime(song.deletedAt),
            'isActive': song.isActive
        }
    
    def _albumSerializer(self, album):
        return {
            'id': album.id,
            'name': album.name,
            'description': album.description,
            'storageImageID': album.storageImageID,
            'artistID': album.artistID,
            'createdAt': self._parseDatetime(album.createdAt),
            'updatedAt': self._parseDatetime(album.updatedAt),
            'deletedAt': self._parseDatetime(album.deletedAt),
            'isActive': album.isActive
        }
    
    def _genreSerializer(self, genre):
        return {
            'id': genre.id,
            'name': genre.name,
            'description': genre.description,
            'createdAt': self._parseDatetime(genre.createdAt),
            'updatedAt': self._parseDatetime(genre.updatedAt),
            'deletedAt': self._parseDatetime(genre.deletedAt),
            'isActive': genre.isActive
        }
    
    def _albumSongSerializer(self, albumSong):
        return {
            'albumID': albumSong.albumID,
            'songID': albumSong.songID,
            'order': albumSong.order,
            'createdAt': self._parseDatetime(albumSong.createdAt),
            'updatedAt': self._parseDatetime(albumSong.updatedAt),
            'deletedAt': self._parseDatetime(albumSong.deletedAt),
            'isActive': albumSong.isActive
        }
    
    def _genreSongSerializer(self, genreSong):
        return {
            'genreID': genreSong.genreID,
            'songID': genreSong.songID,
            'createdAt': self._parseDatetime(genreSong.createdAt),
            'updatedAt': self._parseDatetime(genreSong.updatedAt),
            'deletedAt': self._parseDatetime(genreSong.deletedAt),
            'isActive': genreSong.isActive
        }

    def filterAllSongs(self):
        try:
            grpcResponse = self.stub.filterAllSongs(empty_pb2.Empty())
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            songs = []
            for song in grpcResponse:
                songs.append(self._songSerializer(song))
            return songs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    def getSongById(self, id):
        try:
            grpcResponse = self.stub.getSongById(musicService_pb2.StringRequest(value=id))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._songSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterSongsByTitle(self, title):
        try:
            grpcResponse = self.stub.filterSongsByTitle(musicService_pb2.StringRequest(value=title))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            songs = []
            for song in grpcResponse:
                songs.append(self._songSerializer(song))
            return songs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterSongsByArtistId(self, artistId):
        try:
            grpcResponse = self.stub.filterSongsByArtistId(musicService_pb2.StringRequest(value=artistId))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            songs = []
            for song in grpcResponse:
                songs.append(self._songSerializer(song))
            return songs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterSongsBySongType(self, songType):
        try:
            grpcResponse = self.stub.filterSongsBySongType(musicService_pb2.StringRequest(value=songType))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            songs = []
            for song in grpcResponse:
                songs.append(self._songSerializer(song))
            return songs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def createSong(self, title, artistId, storageId, storageImageId, duration, description, songType):
        try:
            request = musicService_pb2.CreateSongRequest(
                title=title,
                artistId=artistId,
                storageId=storageId,
                storageImageId=storageImageId,
                duration=duration,
                description=description,
                songType=songType
            )
            grpcResponse = self.stub.createSong(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._songSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def updateSong(self, id, title, storageImageId, duration, description, songType):
        try:
            request = musicService_pb2.UpdateSongRequest(
                id=id,
                title=title,
                storageImageId=storageImageId,
                duration=duration,
                description=description,
                songType=songType
            )
            grpcResponse = self.stub.updateSong(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._songSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def deleteSong(self, id):
        try:
            grpcResponse = self.stub.deleteSong(musicService_pb2.StringRequest(value=id))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._songSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterAllAlbums(self):
        try:
            grpcResponse = self.stub.filterAllAlbums(empty_pb2.Empty())
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            albums = []
            for album in grpcResponse:
                albums.append(self._albumSerializer(album))
            return albums, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def getAlbumById(self, id):
        try:
            grpcResponse = self.stub.getAlbumById(musicService_pb2.StringRequest(value=id))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._albumSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterAlbumsByName(self, name):
        try:
            grpcResponse = self.stub.filterAlbumsByName(musicService_pb2.StringRequest(value=name))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            albums = []
            for album in grpcResponse:
                albums.append(self._albumSerializer(album))
            return albums, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterAlbumsByArtistId(self, artistId):
        try:
            grpcResponse = self.stub.filterAlbumsByArtistId(musicService_pb2.StringRequest(value=artistId))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            albums = []
            for album in grpcResponse:
                albums.append(self._albumSerializer(album))
            return albums, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def createAlbum(self, name, description, storageImageId, artistId):
        try:
            request = musicService_pb2.CreateAlbumRequest(
                name=name,
                description=description,
                storageImageId=storageImageId,
                artistId=artistId
            )
            grpcResponse = self.stub.createAlbum(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._albumSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def updateAlbum(self, id, name, description, storageImageId, artistId):
        try:
            request = musicService_pb2.UpdateAlbumRequest(
                id=id,
                name=name,
                description=description,
                storageImageId=storageImageId,
                artistId=artistId
            )
            grpcResponse = self.stub.updateAlbum(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._albumSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def deleteAlbum(self, id):
        try:
            grpcResponse = self.stub.deleteAlbum(musicService_pb2.StringRequest(value=id))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._albumSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterAllGenres(self):
        try:
            grpcResponse = self.stub.filterAllGenres(empty_pb2.Empty())
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            genres = []
            for genre in grpcResponse:
                genres.append(self._genreSerializer(genre))
            return genres, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def getGenreById(self, id):
        try:
            grpcResponse = self.stub.getGenreById(musicService_pb2.StringRequest(value=id))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._genreSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterGenresByName(self, name):
        try:
            grpcResponse = self.stub.filterGenresByName(musicService_pb2.StringRequest(value=name))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            genres = []
            for genre in grpcResponse:
                genres.append(self._genreSerializer(genre))
            return genres, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def createGenre(self, name, description, backgroundImage):
        try:
            request = musicService_pb2.CreateGenreRequest(
                name=name,
                description=description,
                backgroundImage=backgroundImage
            )
            grpcResponse = self.stub.createGenre(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._genreSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def updateGenre(self, id, name, description, backgroundImage):
        try:
            request = musicService_pb2.UpdateGenreRequest(
                id=id,
                name=name,
                description=description,
                backgroundImage=backgroundImage
            )
            grpcResponse = self.stub.updateGenre(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._genreSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def deleteGenre(self, id):
        try:
            grpcResponse = self.stub.deleteGenre(musicService_pb2.StringRequest(value=id))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._genreSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterAllAlbumSongs(self):
        try:
            grpcResponse = self.stub.filterAllAlbumSongs(empty_pb2.Empty())
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            albumSongs = []
            for albumSong in grpcResponse:
                albumSongs.append(self._albumSongSerializer(albumSong))
            return albumSongs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def getAlbumSongByIds(self, albumId, songId):
        try:
            request = musicService_pb2.CreateAlbumSongRequest(
                albumId=albumId,
                songId=songId
            )
            grpcResponse = self.stub.getAlbumSongByIds(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._albumSongSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterAlbumSongsByAlbumId(self, albumId):
        try:
            grpcResponse = self.stub.filterAlbumSongsByAlbumId(musicService_pb2.StringRequest(value=albumId))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            albumSongs = []
            for albumSong in grpcResponse:
                albumSongs.append(self._albumSongSerializer(albumSong))
            return albumSongs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterAlbumSongsBySongId(self, songId):
        try:
            grpcResponse = self.stub.filterAlbumSongsBySongId(musicService_pb2.StringRequest(value=songId))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            albumSongs = []
            for albumSong in grpcResponse:
                albumSongs.append(self._albumSongSerializer(albumSong))
            return albumSongs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def createAlbumSong(self, albumId, songId):
        try:
            request = musicService_pb2.CreateAlbumSongRequest(
                albumId=albumId,
                songId=songId
            )
            grpcResponse = self.stub.createAlbumSong(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._albumSongSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def deleteAlbumSong(self, albumId, songId):
        try:
            request = musicService_pb2.CreateAlbumSongRequest(
                albumId=albumId,
                songId=songId
            )
            grpcResponse = self.stub.deleteAlbumSong(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._albumSongSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterAllGenreSongs(self):
        try:
            grpcResponse = self.stub.filterAllGenreSongs(empty_pb2.Empty())
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            genreSongs = []
            for genreSong in grpcResponse:
                genreSongs.append(self._genreSongSerializer(genreSong))
            return genreSongs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def getGenreSongByIds(self, genreId, songId):
        try:
            request = musicService_pb2.CreateGenreSongRequest(
                genreId=genreId,
                songId=songId
            )
            grpcResponse = self.stub.getGenreSongByIds(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._genreSongSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterGenreSongsByGenreId(self, genreId):
        try:
            grpcResponse = self.stub.filterGenreSongsByGenreId(musicService_pb2.StringRequest(value=genreId))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            genreSongs = []
            for genreSong in grpcResponse:
                genreSongs.append(self._genreSongSerializer(genreSong))
            return genreSongs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterGenreSongsBySongId(self, songId):
        try:
            grpcResponse = self.stub.filterGenreSongsBySongId(musicService_pb2.StringRequest(value=songId))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            genreSongs = []
            for genreSong in grpcResponse:
                genreSongs.append(self._genreSongSerializer(genreSong))
            return genreSongs, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def createGenreSong(self, genreId, songId):
        try:
            request = musicService_pb2.CreateGenreSongRequest(
                genreId=genreId,
                songId=songId
            )
            grpcResponse = self.stub.createGenreSong(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._genreSongSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def deleteGenreSong(self, genreId, songId):
        try:
            request = musicService_pb2.CreateGenreSongRequest(
                genreId=genreId,
                songId=songId
            )
            grpcResponse = self.stub.deleteGenreSong(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._genreSongSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterAllSongSubArtists(self):
        try:
            grpcResponse = self.stub.filterAllSongSubArtists(empty_pb2.Empty())
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            songSubArtists = []
            for songSubArtist in grpcResponse:
                songSubArtists.append(self._songSubArtistSerializer(songSubArtist))
            return songSubArtists, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def getSongSubArtistByIds(self, songId, subArtistId):
        try:
            request = musicService_pb2.CreateSongSubArtistRequest(
                songId=songId,
                subArtistId=subArtistId
            )
            grpcResponse = self.stub.getSongSubArtistByIds(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._songSubArtistSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterSongSubArtistsBySongId(self, songId):
        try:
            grpcResponse = self.stub.filterSongSubArtistsBySongId(musicService_pb2.StringRequest(value=songId))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            songSubArtists = []
            for songSubArtist in grpcResponse:
                songSubArtists.append(self._songSubArtistSerializer(songSubArtist))
            return songSubArtists, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def filterSongSubArtistsBySubArtistId(self, subArtistId):
        try:
            grpcResponse = self.stub.filterSongSubArtistsBySubArtistId(musicService_pb2.StringRequest(value=subArtistId))
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            songSubArtists = []
            for songSubArtist in grpcResponse:
                songSubArtists.append(self._songSubArtistSerializer(songSubArtist))
            return songSubArtists, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def createSongSubArtist(self, songId, subArtistId):
        try:
            request = musicService_pb2.CreateSongSubArtistRequest(
                songId=songId,
                subArtistId=subArtistId
            )
            grpcResponse = self.stub.createSongSubArtist(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._songSubArtistSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    def deleteSongSubArtist(self, songId, subArtistId):
        try:
            request = musicService_pb2.CreateSongSubArtistRequest(
                songId=songId,
                subArtistId=subArtistId
            )
            grpcResponse = self.stub.deleteSongSubArtist(request)
            if grpcResponse is None:
                return None, ErrorCodes.grpcStatusMapping(grpc.RpcError.code())
            return self._songSubArtistSerializer(grpcResponse), None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED
    
    