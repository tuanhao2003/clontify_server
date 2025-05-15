from django.db import models
import uuid
from common.baseEntity import Base
from app.enums.fileTypeEnums import FileTypeEnums

class StorageData(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.UUIDField()
    fileName = models.CharField(max_length=255, unique=True)
    fileType = models.CharField(max_length=255)
    fileSize = models.IntegerField()
    fileUrl = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "app" 