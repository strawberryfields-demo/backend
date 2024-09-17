from django.db import models

from .music import Music
from .user import User


class Pitch(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='pitches')
    agency = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_pitches')
    pitch_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ])