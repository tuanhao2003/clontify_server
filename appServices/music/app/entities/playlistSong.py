from django.db import models
import uuid
from common.baseEntity import Base

class PlaylistSong(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    playlistId = models.UUIDField()
    songId = models.UUIDField()
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        app_label = "app" 