from django_filters import rest_framework as filters
from catalog.models import Item
from django.db.models import JSONField

class UUIDInFilter(filters.BaseInFilter, filters.UUIDFilter):
    pass

class ItemFilter(filters.FilterSet):
    categories = UUIDInFilter(field_name="category", lookup_expr="in")

    class Meta:
        model = Item
        fields = [
            'categories',
            'authors', 'producers', 'contributors',
            'tags', 'rating', 'popularity_score', 'number_of_ratings',
            'created_at', 'updated_at'
        ]
        filter_overrides = {
            JSONField: {
                'filter_class': filters.CharFilter,
            }
        }
