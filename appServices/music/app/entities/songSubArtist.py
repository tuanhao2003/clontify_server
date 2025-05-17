from django.db import models
from common.baseEntity import Base

class SongSubArtist(Base):
    songID = models.UUIDField()
    subArtistID = models.UUIDField()
    
    class Meta:
        app_label = "app" 
        unique_together = ('songID', 'subArtistID')