from rest_framework import serializers
from catalog.models import Category, Item, UserInteraction, Person


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class PersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'bio', 'website')


class PersonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'bio', 'website')

class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'title', 'description', 'category',
            'image', 'url', 'tags',
            'authors', 'contributors', 'producers'
        )

class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'title', 'description', 'category',
            'image', 'url', 'tags',
            'authors', 'contributors', 'producers',
            'popularity_score', 'rating', 'number_of_ratings'
        )

class UserInteractionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = ('id', 'user', 'item', 'interaction_type', 'rating')
        read_only_fields = ('user',)

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
        interaction_type = data.get("interaction_type")

        # Vérifie que les deux existent
        if not interaction_type:
            raise serializers.ValidationError(
                {"interaction_type": "This field is required."}
            )

        if UserInteraction.objects.filter(
            user=user, item=item, interaction_type=interaction_type
        ).exists():
            raise serializers.ValidationError(
                {"detail": f"You already have a '{interaction_type}' interaction with this item."}
            )
        return data

class UserInteractionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = ('rating',)
