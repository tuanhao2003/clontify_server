import uuid
from django.db import models
from django.utils.timezone import now
from accounts import Accounts

class LoginHistories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="LoginHistories")
    ipAddress = models.GenericIPAddressField()
    userAgent = models.TextField(null=True, blank=True)
    loginTime = models.DateTimeField(default=now)
    class Meta:
        app_label = 'app'
