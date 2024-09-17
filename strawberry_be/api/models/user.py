from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 데이터베이스에 저장될 실제 값을 문자열로 정의
    COMPOSER = 'composer'
    AGENCY = 'agency'
    USER_TYPE_CHOICES = [
        (COMPOSER, 'Composer'),
        (AGENCY, 'Agency'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    bio = models.TextField(blank=True)