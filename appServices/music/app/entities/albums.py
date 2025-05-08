from django.db import models
import uuid
from common.baseEntity import Base

class Albums(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    storageImageId = models.UUIDField(null=True, blank=True)
    artistId = models.UUIDField()

    class Meta:
        app_label = "app" 