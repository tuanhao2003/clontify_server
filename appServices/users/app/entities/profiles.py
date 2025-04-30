import uuid
from django.db import models
from common.baseEntity import Base

class Profiles(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountID = models.UUIDField(unique=True)
    fullName = models.TextField(max_length=150, blank=False, null=False, default="noname")
    avatarUrl = models.URLField(blank=True, null=True)
    bio = models.TextField(max_length=500,blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True) 

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = "app"