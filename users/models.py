from django.db import models
from django.contrib.auth.models import AbstractUser


# Class roles
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Custom user model with roles
class CustomUser(AbstractUser):
    roles = models.ManyToManyField(roles, blank=True)
