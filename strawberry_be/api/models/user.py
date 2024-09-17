import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from api.models import error


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(error.USER_MODEL_ERRORS["email"]["required"])

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    objects = UserManager()

    # 작곡가 보안을 위해 UUID 사용
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(
        max_length=25,
    )
    phone = PhoneNumberField(blank=True)

    COMPOSER = "Composer"
    AGENCY = "Agency"

    USER_TYPE_CHOICES = [(COMPOSER, COMPOSER), (AGENCY, AGENCY)]
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default=COMPOSER
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "phone",
        "user_type",
    ]
