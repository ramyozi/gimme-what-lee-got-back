from rest_framework import serializers

from accounts.serializers.read import AccountSerializer
from catalog.models import Category, Item, UserInteraction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    created_by = AccountSerializer(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'

class UserInteractionSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = UserInteraction
        fields = '__all__'
