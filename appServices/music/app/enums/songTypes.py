from django.db import models

class SongTypes(models.TextChoices):
    SONG = 'SONG', 'Song'
    MUSIC_VIDEO = 'MUSIC_VIDEO', 'Music Video' 