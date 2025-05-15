import uuid
from django.db import models
from common.baseEntity import Base

class Favorites(Base):
    profileID = models.UUIDField()
    songID = models.UUIDField()

    class Meta:
        app_label = "app"
        unique_together = ('profileID', 'songID')