from django.db import models

class FileTypeEnums(models.TextChoices):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'