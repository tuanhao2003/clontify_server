from rest_framework import serializers
from app.entities.playlists import Playlists

class PlaylistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlists
        fields = '__all__' 