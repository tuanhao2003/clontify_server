from django.db import models
import uuid
from common.baseEntity import Base

class Genres(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "app" 