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

    """
    Lors de la création, l'utilisateur est automatiquement
    associé via la requête donc pas besoin que le frontend envoie un user_id.
    """
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    """
    Vérifie qu'il n'existe pas déjà une interaction (user, item).
    """
    def validate(self, data):
        user = self.context['request'].user
        item = data.get('item')

        if UserInteraction.objects.filter(user=user, item=item).exists():
            raise serializers.ValidationError(
                {"detail": "You already have an interaction with this item."}
            )
        return data

class UserInteractionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = ('liked', 'bookmarked', 'rating')
