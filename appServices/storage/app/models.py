from django.db import models
import uuid

# Create your models here.

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fileName = models.CharField(max_length=255)
    fileType = models.CharField(max_length=50)  # audio, image, video
    fileSize = models.BigIntegerField()  # in bytes
    s3Key = models.CharField(max_length=255)  # S3 object key
    s3Bucket = models.CharField(max_length=255)  # S3 bucket name
    s3Url = models.URLField(max_length=500)  # S3 URL
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = 'files'
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.fileName} ({self.fileType})"
