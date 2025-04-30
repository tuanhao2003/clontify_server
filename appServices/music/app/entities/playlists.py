from django.db import models
import uuid
from common.baseEntity import Base

class Playlists(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ownerId = models.UUIDField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = "app" 