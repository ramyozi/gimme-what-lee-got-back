from rest_framework import routers
from .views import CategoryViewSet, ItemViewSet, UserInteractionViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)
router.register(r'interactions', UserInteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
