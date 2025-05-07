from rest_framework import serializers
from app.entities.storageData import StorageData

class StorageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageData
        fields = '__all__' 