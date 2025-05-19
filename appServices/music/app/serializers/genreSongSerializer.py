from rest_framework import serializers
from app.entities.genreSong import GenreSong

class GenreSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreSong
        fields = '__all__' 