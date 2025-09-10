from django.db import models
from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):
    USER = "user", "User"
    ADMIN = "admin", "Admin"

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.USER
    )

    def is_admin(self):
        return self.role == RoleChoices.ADMIN
