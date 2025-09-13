from rest_framework import serializers
from catalog.models import Category, Item, UserInteraction

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description')

class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description')

class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'title', 'description', 'category',
            'image', 'url', 'tags'
        )

class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'title', 'description', 'category',
            'image', 'url', 'tags',
            'popularity_score', 'rating', 'number_of_ratings'
        )

class UserInteractionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = ('user', 'item', 'liked', 'bookmarked', 'rating')

class UserInteractionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = ('liked', 'bookmarked', 'rating')
