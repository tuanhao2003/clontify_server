from rest_framework import serializers
from app.entities.genres import Genres

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__' 