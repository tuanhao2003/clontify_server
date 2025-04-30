from rest_framework import serializers
from app.entities.songs import Songs

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = '__all__' 