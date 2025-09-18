from django_filters import rest_framework as filters
from catalog.models import Item
from django.db.models import JSONField

class ItemFilter(filters.FilterSet):
    class Meta:
        model = Item
        fields = [
            'category', 'authors', 'producers', 'contributors',
            'tags', 'rating', 'popularity_score', 'number_of_ratings',
            'created_at', 'updated_at'
        ]
        filter_overrides = {
            JSONField: {
                'filter_class': filters.CharFilter,
            }
        }
