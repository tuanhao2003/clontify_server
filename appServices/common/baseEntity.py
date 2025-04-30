from django.db import models
from django.utils.timezone import now

class Base(models.Model):
    createdAt = models.DateTimeField(default=now)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        abstract = True