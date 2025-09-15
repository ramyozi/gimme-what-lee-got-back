from rest_framework import routers
from catalog.views import CategoryViewSet, ItemViewSet, UserInteractionViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'item', ItemViewSet)
router.register(r'interaction', UserInteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
