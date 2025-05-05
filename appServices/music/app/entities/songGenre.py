from django.db import models
import uuid
from common.baseEntity import Base

class SongGenre(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    songID = models.UUIDField()
    genreID = models.UUIDField()
    
    def __str__(self):
        return self.id