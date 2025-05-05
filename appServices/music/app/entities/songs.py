from django.db import models
import uuid
from common.baseEntity import Base

class Songs(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(blank=True, null= True)
    artistId = models.UUIDField()
    audioUrl = models.URLField()
    backgroundImage = models.URLField(blank=True, null=True)
    duration = models.PositiveIntegerField()
    pending = models.BooleanField(default=True)
    
    def __str__(self):
        return self.id