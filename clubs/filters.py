import django_filters
from clubs.models import Club


class ClubFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Club Name')
    description = django_filters.CharFilter(lookup_expr='icontains', label='Description')

    class Meta:
        model = Club
        fields = ['name', 'description']
