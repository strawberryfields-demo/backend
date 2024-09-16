from django.db import models

from strawberry_be.strawberry_be.models.music import Music
from strawberry_be.strawberry_be.models.user import User


class Pitch(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='pitches')
    agency = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_pitches')
    pitch_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ])