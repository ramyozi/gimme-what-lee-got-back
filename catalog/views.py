import numpy as np
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, generics, filters
from rest_framework.decorators import action
from rest_framework import generics, filters as drf_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from catalog.filters import ItemFilter
from catalog.models import Category, Item, UserInteraction, Person
from catalog.pagination import CustomPageNumberPagination
from catalog.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from catalog.serializers.read import (
    CategorySerializer, ItemSerializer, UserInteractionSerializer, PersonSerializer
)
from catalog.serializers.write import (
    CategoryCreateSerializer, CategoryUpdateSerializer,
    ItemCreateSerializer, ItemUpdateSerializer,
    UserInteractionCreateSerializer, UserInteractionUpdateSerializer, PersonCreateSerializer, PersonUpdateSerializer,
)


# Gestion des catégories
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return CategoryCreateSerializer
        if self.action in ["update", "partial_update"]:
            return CategoryUpdateSerializer
        return CategorySerializer

# Gestion des personnes
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return PersonCreateSerializer
        if self.action in ["update", "partial_update"]:
            return PersonUpdateSerializer
        return PersonSerializer

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

    @action(detail=False, methods=["get"], url_path="recommendations", permission_classes=[IsAuthenticated])
    def recommendations(self, request):
        """
        Recommande des items similaires à ceux aimés ou enregistrés par l'utilisateur,
        en utilisant la similarité vectorielle (TF-IDF + similarité cosinus).
        """
        user = request.user

        # Récupère les items que l'utilisateur a likés ou ajoutés en favoris
        user_items = Item.objects.filter(
            userinteraction__user=user,
            userinteraction__interaction_type__in=["like", "bookmark"]
        ).distinct()

        # Si l'utilisateur n'a encore rien aimé, renvoyer les plus populaires
        if not user_items.exists():
            fallback = Item.objects.all().order_by("-popularity_score", "-rating")[:10]
            serializer = ItemSerializer(fallback, many=True)
            return Response(serializer.data)

        # Crée un corpus textuel pour tous les items (titre, description, tags, catégorie)
        items = Item.objects.all().select_related("category")
        corpus = []
        for item in items:
            tags_text = " ".join(item.tags or [])
            category_name = item.category.name if item.category else ""
            text = f"{item.title} {item.description} {tags_text} {category_name}"
            corpus.append(text)

        # Convertit le texte en vecteurs numériques avec TF-IDF
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Crée un vecteur moyen représentant les préférences de l'utilisateur
        user_indices = [list(items).index(i) for i in user_items if i in items]
        if not user_indices:
            fallback = Item.objects.all().order_by("-popularity_score", "-rating")[:10]
            serializer = ItemSerializer(fallback, many=True)
            return Response(serializer.data)

        user_vector = np.mean(tfidf_matrix[user_indices].toarray(), axis=0).reshape(1, -1)

        # Calcule la similarité cosinus entre le vecteur utilisateur et tous les items
        similarities = cosine_similarity(user_vector, tfidf_matrix)[0]

        # Trie les items selon leur score de similarité
        scored_items = list(zip(items, similarities))
        scored_items.sort(key=lambda x: x[1], reverse=True)

        # Exclut les items déjà likés ou favoris et garde les plus proches
        recommended = [i for i, score in scored_items if i not in user_items][:20]

        # Sérialise et renvoie les résultats
        serializer = ItemSerializer(recommended, many=True)
        return Response(serializer.data)

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

    # Interactions d'un utilisateur pour un item donné
    @action(detail=False, methods=["get"], url_path="user/(?P<user_id>[^/.]+)/item/(?P<item_id>[^/.]+)")
    def interactions_for_item(self, request, user_id=None, item_id=None):
        """
        Renvoie toutes les interactions d'un utilisateur pour un item donné.
        """
        interactions = UserInteraction.objects.filter(user_id=user_id, item_id=item_id)
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)


# API endpoint for catalog search with filters, pagination, sorting
class ItemSearchView(generics.ListAPIView):
    queryset = Item.objects.all()
    permission_classes = [permissions.AllowAny]

    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]

    filterset_class = ItemFilter  # <-- use custom filter

    search_fields = ['title', 'description']  # search by text
    ordering_fields = ['created_at', 'updated_at', 'rating', 'popularity_score', 'number_of_ratings']
    pagination_class = CustomPageNumberPagination