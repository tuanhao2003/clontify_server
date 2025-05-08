from django.contrib import admin
from django.urls import path
from app.controllers.albumsController import *
from app.controllers.songsController import *
from app.controllers.genresController import *

urlpatterns = [
    path('admin', admin.site.urls),
    
    path('album/create', CreateAlbum.as_view(), name='create_album'),
    path('album/update', UpdateAlbum.as_view(), name='update_album'),
    path('album/delete', DeleteAlbum.as_view(), name='delete_album'),
    path('album/<str:id>', GetAlbums.as_view(), name='get_album_by_id'),
    path('albums', GetAlbums.as_view(), name='get_albums'),
    
    path('song/create', CreateSong.as_view(), name='create_song'),
    path('song/update', UpdateSong.as_view(), name='update_song'),
    path('song/delete', DeleteSong.as_view(), name='delete_song'),
    path('song/<str:id>', GetSongs.as_view(), name='get_song_by_id'),
    path('songs', GetSongs.as_view(), name='get_songs'),
    
    path('genre/create', CreateGenre.as_view(), name='create_genre'),
    path('genre/update', UpdateGenre.as_view(), name='update_genre'),
    path('genre/delete', DeleteGenre.as_view(), name='delete_genre'),
    path('genre/<str:id>', GetGenres.as_view(), name='get_genre_by_id'),
    path('genres', GetGenres.as_view(), name='get_genres'),
]
