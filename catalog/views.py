from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from catalog.models import Category, Item, UserInteraction
from catalog.serializers.read import (
    CategorySerializer, ItemSerializer, UserInteractionSerializer
)
from catalog.serializers.write import (
    CategoryCreateSerializer, CategoryUpdateSerializer,
    ItemCreateSerializer, ItemUpdateSerializer,
    UserInteractionCreateSerializer, UserInteractionUpdateSerializer,
)
from accounts.decorators import allowed_roles

# viewset pour gérer les catégories
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CategoryCreateSerializer
        if self.action in ["update", "partial_update"]:
            return CategoryUpdateSerializer
        return CategorySerializer

    # seules les admins peuvent créer/modifier/supprimer
    @allowed_roles("admin")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @allowed_roles("admin")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @allowed_roles("admin")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allowed_roles("admin")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# viewset pour gérer les items
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ItemCreateSerializer
        if self.action in ["update", "partial_update"]:
            return ItemUpdateSerializer
        return ItemSerializer

    # seules les admins peuvent créer/modifier/supprimer
    @allowed_roles("admin")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @allowed_roles("admin")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @allowed_roles("admin")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allowed_roles("admin")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# viewset pour gérer les interactions utilisateur
class UserInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserInteraction.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserInteractionCreateSerializer
        if self.action in ["update", "partial_update"]:
            return UserInteractionUpdateSerializer
        return UserInteractionSerializer

    # seuls les membres et admins peuvent créer une interaction
    @allowed_roles("member", "admin")
    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id  # forcer l'utilisateur connecté
        return super().create(request, *args, **kwargs)

    # membres peuvent modifier uniquement leurs propres interactions
    @allowed_roles("member", "admin")
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user and request.user.role != "admin":
            return Response({"detail": "Permission denied"}, status=403)
        return super().update(request, *args, **kwargs)

    @allowed_roles("member", "admin")
    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user and request.user.role != "admin":
            return Response({"detail": "Permission denied"}, status=403)
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='liked-items/(?P<user_id>[^/.]+)')
    def liked_items(self, request, user_id=None):
        interactions = UserInteraction.objects.filter(user_id=user_id, liked=True)
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='bookmarked-items/(?P<user_id>[^/.]+)')
    def bookmarked_items(self, request, user_id=None):
        interactions = UserInteraction.objects.filter(user_id=user_id, bookmarked=True)
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)
