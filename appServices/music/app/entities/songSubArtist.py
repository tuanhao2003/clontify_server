from django.db import models
from common.baseEntity import Base

class SongSubArtist(Base):
    songID = models.UUIDField()
    subArtistID = models.UUIDField()
    
    def __str__(self):
        return self.id