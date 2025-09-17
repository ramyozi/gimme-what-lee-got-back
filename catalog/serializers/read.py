from rest_framework import serializers

from accounts.serializers.read import AccountSerializer
from catalog.models import Category, Item, UserInteraction, Person


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "name", "bio", "website"]

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    created_by = AccountSerializer(read_only=True)
    authors = PersonSerializer(read_only=True, many=True)
    contributors = PersonSerializer(read_only=True, many=True)
    producers = PersonSerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = '__all__'

class UserInteractionSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = UserInteraction
        fields = '__all__'
