from django.contrib import admin
from django.urls import path
from app.controllers.albumsController import *
from app.controllers.songsController import *
from app.controllers.genresController import *

urlpatterns = [
    path('admin', admin.site.urls),
    path('albums', GetAlbums.as_view(), name='get_albums'),
    path('albums/<uuid:id>', GetAlbums.as_view(), name='get_album_by_id'),
    path('albums/create', CreateAlbum.as_view(), name='create_album'),
    path('albums/update', UpdateAlbum.as_view(), name='update_album'),
    path('albums/delete', DeleteAlbum.as_view(), name='delete_album'),
    path('song/<uuid:id>', GetSongs.as_view(), name='get_albums_by_song_id'),
    path('song/create', CreateSong.as_view(), name='create_song'),
    path('song/update', UpdateSong.as_view(), name='update_song'),
    path('song/delete', DeleteSong.as_view(), name='delete_song'),
    path('genres', GetGenres.as_view(), name='get_genres'),
    path('genres/<uuid:id>', GetGenres.as_view(), name='get_genre_by_id'),
    path('genres/create', CreateGenre.as_view(), name='create_genre'),
    path('genres/update', UpdateGenre.as_view(), name='update_genre'),
    path('genres/delete', DeleteGenre.as_view(), name='delete_genre'),
]
