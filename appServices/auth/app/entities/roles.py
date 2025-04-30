import uuid
from django.db import models
from common.baseEntity import Base

class Roles(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        app_label = "app"