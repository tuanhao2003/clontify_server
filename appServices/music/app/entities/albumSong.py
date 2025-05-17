from django.db import models
import uuid
from common.baseEntity import Base

class AlbumSong(Base):
    albumId = models.UUIDField()
    songId = models.UUIDField()
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        app_label = "app" 
        unique_together = ('albumId', 'songId')