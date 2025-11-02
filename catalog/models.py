import uuid
from django.db import models
from accounts.models import Account


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    image = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='items_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.JSONField(default=list, blank=True)
    popularity_score = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    number_of_ratings = models.PositiveIntegerField(default=0)
    authors = models.ManyToManyField(Person, blank=True, related_name="authored_items")
    producers = models.ManyToManyField(Person, blank=True, related_name="produced_items")
    contributors = models.ManyToManyField(Person, blank=True, related_name="contributed_items")

    class Meta:
        ordering = ["-popularity_score", "-created_at"]

    def __str__(self):
        return self.title


class UserInteraction(models.Model):
    class InteractionType(models.TextChoices):
        LIKE = "like", "Like"
        BOOKMARK = "bookmark", "Bookmark"
        RATING = "rating", "Rating"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    interaction_type = models.CharField(
        max_length=20,
        choices=InteractionType.choices,
        default=InteractionType.LIKE
    )
    rating = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "item", "interaction_type")
        indexes = [
            models.Index(fields=["user", "item", "interaction_type"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.item.title}"