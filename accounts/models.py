from django.db import models
from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):
    MEMBER = "member", "Member"
    ADMIN = "admin", "Admin"

class Account(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.MEMBER
    )

    def is_admin(self):
        return self.role == RoleChoices.ADMIN

    # surcharge de is_staff pour que les admins aient accès à l'admin Django
    @property
    def is_staff(self):
        return self.is_admin()
