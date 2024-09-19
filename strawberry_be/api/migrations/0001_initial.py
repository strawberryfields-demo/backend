# Generated by Django 4.2.16 on 2024-09-17 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("username", models.EmailField(max_length=25)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[("Composer", "Composer"), ("Agency", "Agency")],
                        default="Composer",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("deleted_at", models.DateTimeField(null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Music",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("composer", models.CharField(max_length=100)),
                ("genre", models.CharField(max_length=50)),
                ("duration", models.IntegerField(help_text="Duration in seconds")),
                ("file_path", models.URLField(max_length=500)),
                (
                    "file_type",
                    models.CharField(
                        choices=[("mp3", "MP3"), ("wav", "WAV")], max_length=5
                    ),
                ),
                ("upload_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("uploaded", "Uploaded"),
                            ("pitched", "Pitched"),
                            ("accepted", "Accepted"),
                        ],
                        max_length=20,
                    ),
                ),
                ("lyrics", models.TextField(blank=True)),
                ("bpm", models.IntegerField(blank=True, null=True)),
                ("key", models.CharField(blank=True, max_length=10)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pitch",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pitch_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("rejected", "Rejected"),
                            ("accepted", "Accepted"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "agency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "music",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.music"
                    ),
                ),
            ],
        ),
    ]
