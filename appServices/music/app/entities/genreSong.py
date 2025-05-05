from django.db import models
import uuid
from common.baseEntity import Base

class GenreSong(Base):
    songID = models.UUIDField()
    genreID = models.UUIDField()
    
    def __str__(self):
        return self.id