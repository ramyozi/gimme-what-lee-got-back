from django.shortcuts import render
from rest_framework import viewsets

from catalog.models import Category, Item, UserInteraction
from catalog.serializers import CategorySerializer, ItemSerializer, UserInteractionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class UserInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserInteraction.objects.all()
    serializer_class = UserInteractionSerializer

    @action(detail=False, methods=['get'], url_path='liked-items/(?P<user_id>[^/.]+)')
    def liked_items(self, request, user_id:None):
        """Return all liked items for a specific user."""
        interactions = UserInteraction.objects.filter(user_id=user_id, liked=True)
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='bookmarked-items/(?P<user_id>[^/.]+)')
    def bookmarked_items(self, request, user_id: None):
        """Return all bookmarked items for a specific user."""
        interactions = UserInteraction.objects.filter(user_id=user_id, bookmarked=True)
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)
