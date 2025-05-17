from rest_framework import serializers
from app.entities.songs import Songs
from app.grpc.grpcClients.storageGrpcClient import StorageGrpcClient

class SongsSerializer(serializers.ModelSerializer):
    songUrl = serializers.SerializerMethodField()
    backgroundUrl = serializers.SerializerMethodField()

    class Meta:
        model = Songs
        exclude = ('storageId', 'storageImageId')

    def get_songUrl(self, obj):
        if not obj.storageId:
            return None
        try:
            client = StorageGrpcClient()
            storageData, error = client.findById(str(obj.storageId))
            if error:
                return str(error)
            url, error = client.genPublicUrl(storageData.fileUrl)
            if error:
                return None
            return url
        except Exception:
            return None
        finally:
            client.close()

    def get_backgroundUrl(self, obj):
        if not obj.storageImageId:
            return None
        try:
            client = StorageGrpcClient()
            storageData, error = client.findById(str(obj.storageImageId))
            if error:
                return None
            url, error = client.genPublicUrl(storageData.fileUrl)
            if error:
                return None
            return url
        except Exception:
            return None
        finally:
            client.close()
