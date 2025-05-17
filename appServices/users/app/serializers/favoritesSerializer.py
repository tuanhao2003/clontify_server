from rest_framework import serializers
from app.entities.favorites import Favorites
 
class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__' 