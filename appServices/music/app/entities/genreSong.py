from django.db import models
import uuid
from common.baseEntity import Base

class GenreSong(Base):
    songID = models.UUIDField()
    genreID = models.UUIDField()
    
    class Meta:
        app_label = "app" 
        unique_together = ('songID', 'genreID')