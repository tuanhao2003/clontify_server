from django.db import models
import uuid
from common.baseEntity import Base

class StorageData(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.UUIDField()
    fileName = models.CharField(max_length=255)
    fileType = models.CharField(max_length=255)
    fileSize = models.IntegerField()
    fileUrl = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        app_label = "app" 