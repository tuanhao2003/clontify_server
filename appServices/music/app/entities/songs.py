from django.db import models
import uuid
from common.baseEntity import Base
from app.enums.songTypes import SongTypes

class Songs(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(blank=True, null= True)
    artistId = models.UUIDField()
    storageId = models.UUIDField(unique=True, null=False, blank=False)
    storageImageId = models.UUIDField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    songType = models.CharField(max_length=255, choices=SongTypes.choices)
    class Meta:
        app_label = "app" 