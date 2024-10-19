from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Video(models.Model):
    id=models.AutoField(primary_key=True)
    video = models.FileField(upload_to='videos_uploaded',null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])

    def __str__(self):
        return self.name
    
class Subtitle(models.Model):
    id = models.AutoField(primary_key=True)
    subtitle = models.FileField(upload_to='subtitles_uploaded', null=True, validators=[FileExtensionValidator(allowed_extensions=['srt','vtt','sub','sbv'])])
    video = models.ForeignKey(Video, on_delete=models.CASCADE)  # Assuming each subtitle is linked to a video
    def __str__(self):
        return self.name
    
class CorrectSubtitles(models.Model):
    id = models.AutoField(primary_key=True)
    subtitle = models.FileField(upload_to='subtitles_uploaded', null=True, validators=[FileExtensionValidator(allowed_extensions=['srt','vtt','sub','sbv'])])
    video = models.ForeignKey(Video, on_delete=models.CASCADE)  # Assuming each subtitle is linked to a video
    def __str__(self):
        return self.name
