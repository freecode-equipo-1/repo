from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    # el usuario será el email
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email: models.EmailField = models.EmailField(
        max_length=256,
        unique=True,
    )
    first_name = models.CharField(
        max_length=256,
        blank=False,
    )
    last_name = models.CharField(
        max_length=256,
        blank=False,
    )
    password = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.email
