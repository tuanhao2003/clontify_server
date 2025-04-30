from rest_framework import serializers
from app.entities.playlistSong import PlaylistSong

class PlaylistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistSong
        fields = '__all__' 