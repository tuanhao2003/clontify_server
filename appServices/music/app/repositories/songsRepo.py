from django.utils.timezone import now
from app.entities.songs import Songs
from app.entities.genreSong import GenreSong
from app.entities.songSubArtist import SongSubArtist
from app.entities.albumSong import AlbumSong
from django.core.paginator import Paginator
from django.db import models
import uuid

class SongsRepo:
    @staticmethod
    def findAllPaginated(page: int = 1, pageSize: int = 10):
        try:
            result = Songs.objects.filter(isActive=True)
            paginator = Paginator(result, pageSize)
            return {
                'result': paginator.get_page(page),
                'total': paginator.count,
                'totalPages': paginator.num_pages,
                'currentPage': page
            }
        except Exception:
            return None

    @staticmethod
    def findAll():
        try:
            return Songs.objects.filter(isActive=True)
        except Exception:
            return None

    @staticmethod
    def getById(id: uuid.UUID):
        try:
            return Songs.objects.get(id=id, isActive=True)
        except Exception:
            return None
    
    @staticmethod
    def getByIds(ids: list[uuid.UUID]):
        try:
            return Songs.objects.filter(id__in=ids, isActive=True)
        except Exception:
            return None

    @staticmethod
    def filterByTitlePaginated(title: str, page: int = 1, pageSize: int = 10):
        try:
            result = Songs.objects.filter(title__icontains=title, isActive=True)
            paginator = Paginator(result, pageSize)
            return {
                'result': paginator.get_page(page),
                'total': paginator.count,
                'totalPages': paginator.num_pages,
                'currentPage': page
            }
        except Exception:
            return None

    @staticmethod
    def filterByTitle(title: str):
        try:
            return Songs.objects.filter(title__icontains=title, isActive=True)
        except Exception:
            return None
        
    @staticmethod
    def findByArtistId(artistId: uuid.UUID):
        try:
            ownedSongs = Songs.objects.filter(artistId=artistId, isActive=True)
            participatedSongIds = SongSubArtist.objects.filter(subArtistID=artistId).values_list('songID', flat=True)
            participatedSongs = Songs.objects.filter(id__in=participatedSongIds, isActive=True)
            result = (ownedSongs | participatedSongs).distinct()
            return result
        except Exception:
            return None

    @staticmethod
    def findByArtistIdPaginated(artistId: uuid.UUID, page: int = 1, pageSize: int = 10):
        try:
            ownedSongs = Songs.objects.filter(artistId=artistId, isActive=True)
            participatedSongIds = SongSubArtist.objects.filter(subArtistID=artistId).values_list('songID', flat=True)
            participatedSongs = Songs.objects.filter(id__in=participatedSongIds, isActive=True)
            result = (ownedSongs | participatedSongs).distinct()
            paginator = Paginator(result, pageSize)
            return {
                'result': paginator.get_page(page),
                'total': paginator.count,
                'totalPages': paginator.num_pages,
                'currentPage': page
            }
        except Exception:
            return None

    @staticmethod
    def create(song: Songs):
        try:
            song.save()
            return song
        except Exception:
            return None

    @staticmethod
    def update(song: Songs):
        try:
            song.updatedAt = now()
            song.save()
            return song
        except Exception:
            return None

    @staticmethod
    def delete(song: Songs):
        try:
            song.isActive = False
            song.deletedAt = now()
            song.save()
            return song
        except Exception:
            return None