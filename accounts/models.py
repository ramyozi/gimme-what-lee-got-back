import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):
    MEMBER = "member", "Member"
    ADMIN = "admin", "Admin"

class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    @is_staff.setter
    def is_staff(self, value):
        # Ignorer ou convertir en rôle admin
        if value:
            self.role = "admin"
        else:
            self.role = "member"

