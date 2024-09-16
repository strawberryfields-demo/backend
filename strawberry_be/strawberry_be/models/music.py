from django.db import models

from strawberry_be.strawberry_be.models.user import User


class Music(models.Model):
    title = models.CharField(max_length=200)
    composer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compositions')
    genre = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="Duration in seconds")
    file_path = models.URLField(max_length=500)
    file_type = models.CharField(max_length=5, choices=[('mp3', 'MP3'), ('wav', 'WAV')])
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('uploaded', 'Uploaded'),
        ('pitched', 'Pitched'),
        ('accepted', 'Accepted')
    ])
    lyrics = models.TextField(blank=True)
    bpm = models.IntegerField(null=True, blank=True)
    key = models.CharField(max_length=10, blank=True)
