from rest_framework import serializers
from app.entities.albumSong import AlbumSong

class AlbumSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumSong
        fields = '__all__' 