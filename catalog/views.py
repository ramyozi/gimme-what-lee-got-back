from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, generics, filters
from rest_framework.decorators import action
from rest_framework import generics, filters as drf_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from catalog.filters import ItemFilter
from catalog.models import Category, Item, UserInteraction
from catalog.pagination import CustomPageNumberPagination
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

    # feed
    @action(detail=False, methods=["get"], url_path="feed")
    def feed(self,request):
        """
        Retourne un "feed" des items, triés par popularité (ou autre critère).
        Plus tard, on pourra ajouter des recommandations personnalisées.
        """
        items = (
            Item.objects.all()
            .select_related("category", "created_by")
            .order_by("-popularity_score", "-created_at") #[:50] pour le top 50
        )
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated], url_path="like")
    def like(self, request, pk=None):
        """
        Toggle like pour l'utilisateur connecté sur l'item pk.
        Retourne l'état de l'interaction.
        """
        item = self.get_object()
        user = request.user
        interaction, created = UserInteraction.objects.get_or_create(user=user, item=item)
        interaction.liked = not interaction.liked
        interaction.save()
        return Response({"liked": interaction.liked}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated], url_path="bookmark")
    def bookmark(self, request, pk=None):
        """
        Toggle bookmark pour l'utilisateur connecté sur l'item pk.
        """
        item = self.get_object()
        user = request.user
        interaction, created = UserInteraction.objects.get_or_create(user=user, item=item)
        interaction.bookmarked = not interaction.bookmarked
        interaction.save()
        return Response({"bookmarked": interaction.bookmarked}, status=status.HTTP_200_OK)

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
        interactions = UserInteraction.objects.filter(
            user_id=user_id, interaction_type="like"
        ).select_related("item")
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    # Items bookmarkés par un utilisateur
    @action(detail=False, methods=["get"], url_path="bookmarked-items/(?P<user_id>[^/.]+)")
    def bookmarked_items(self, request, user_id=None):
        interactions = UserInteraction.objects.filter(
            user_id=user_id, interaction_type="bookmark"
        ).select_related("item")
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)

# API endpoint for catalog search with filters, pagination, sorting
class ItemSearchView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]

    filterset_class = ItemFilter  # <-- use custom filter

    search_fields = ['title', 'description']  # search by text
    ordering_fields = ['created_at', 'updated_at', 'rating', 'popularity_score', 'number_of_ratings']
    pagination_class = CustomPageNumberPagination