from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from catalog.models import Category, Item, UserInteraction
from catalog.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from catalog.serializers.read import (
    CategorySerializer, ItemSerializer, UserInteractionSerializer
)
from catalog.serializers.write import (
    CategoryCreateSerializer, CategoryUpdateSerializer,
    ItemCreateSerializer, ItemUpdateSerializer,
    UserInteractionCreateSerializer, UserInteractionUpdateSerializer,
)


# Gestion des catégories
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]  # seuls admins modifient

    def get_serializer_class(self):
        if self.action == "create":
            return CategoryCreateSerializer
        if self.action in ["update", "partial_update"]:
            return CategoryUpdateSerializer
        return CategorySerializer


# Gestion des items
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    permission_classes = [IsAdminOrReadOnly]  # seuls admins modifient

    def get_serializer_class(self):
        if self.action == "create":
            return ItemCreateSerializer
        if self.action in ["update", "partial_update"]:
            return ItemUpdateSerializer
        return ItemSerializer


# Gestion des interactions utilisateur
class UserInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserInteraction.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserInteractionCreateSerializer
        if self.action in ["update", "partial_update"]:
            return UserInteractionUpdateSerializer
        return UserInteractionSerializer

    def get_permissions(self):
        # création = utilisateur connecté requis
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        # update/destroy = propriétaire ou admin
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        # lecture libre
        return [permissions.AllowAny()]

    # Items likés par un utilisateur
    @action(detail=False, methods=["get"], url_path="liked-items/(?P<user_id>[^/.]+)")
    def liked_items(self, request, user_id=None):
        interactions = (
            UserInteraction.objects.filter(user_id=user_id, liked=True)
            .select_related("item")  # optimisation DB
        )
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    # Items bookmarkés par un utilisateur
    @action(detail=False, methods=["get"], url_path="bookmarked-items/(?P<user_id>[^/.]+)")
    def bookmarked_items(self, request, user_id=None):
        interactions = (
            UserInteraction.objects.filter(user_id=user_id, bookmarked=True)
            .select_related("item")
        )
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)
