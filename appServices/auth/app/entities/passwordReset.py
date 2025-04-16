import uuid
from django.db import models
from accounts import Accounts
from common.baseEntity import Base


class PasswordResets(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="PasswordResets")
    resetToken = models.TextField()
    expires = models.DateTimeField()
    class Meta:
        app_label = 'app'
