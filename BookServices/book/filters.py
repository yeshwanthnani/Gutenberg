import django_filters
from .models import *

class BooksBookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    media_type = django_filters.CharFilter(lookup_expr='iexact')
    download_count = django_filters.NumberFilter()
    download_count__gte = django_filters.NumberFilter(field_name='download_count', lookup_expr='gte')
    download_count__lte = django_filters.NumberFilter(field_name='download_count', lookup_expr='lte')

    class Meta:
        model = BooksBook
        fields = ['title', 'media_type', 'download_count']
