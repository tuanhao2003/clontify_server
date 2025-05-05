import uuid
from django.db import models
from common.baseEntity import Base
from app.entities.roles import Roles


class Accounts(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roleId = models.UUIDField()
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.TextField()

    def __str__(self):
        return self.id

    class Meta:
        app_label = "app"
