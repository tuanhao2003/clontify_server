import uuid
from django.db import models
from common.baseEntity import Base


class Accounts(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.TextField()
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        app_label = "app"
