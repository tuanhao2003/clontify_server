from rest_framework import serializers
from app.entities.albums import Albums

class AlbumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Albums
        fields = '__all__' 