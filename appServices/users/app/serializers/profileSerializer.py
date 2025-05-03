from rest_framework import serializers
from app.entities.profiles import Profiles
 
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = '__all__' 