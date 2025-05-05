from django.db import models
import uuid
from common.baseEntity import Base

class SongGenre(Base):
    songID = models.UUIDField()
    subArtistID = models.UUIDField()
    
    def __str__(self):
        return self.id