from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.JSONField(default=list, blank=True)
    popularity_score = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    number_of_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'item')
