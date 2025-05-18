from rest_framework import serializers
from app.entities.albums import Albums
from app.grpc.grpcClients.storageGrpcClient import StorageGrpcClient

class AlbumsSerializer(serializers.ModelSerializer):
    backgroundUrl = serializers.SerializerMethodField()
    class Meta:
        model = Albums
        fields = '__all__' 

    def get_backgroundUrl(self, obj):
        if not obj.storageImageId:
            return None
        try:
            client = StorageGrpcClient()
            storageData, error = client.findById(str(obj.storageImageId))
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