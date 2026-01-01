import django_filters
from memberships.models import Membership


class MemberFilter(django_filters.FilterSet):
    user__username = django_filters.CharFilter(lookup_expr='icontains', label='Username')
    role = django_filters.ChoiceFilter(choices=Membership.ROLE_CHOICES, label='Role')

    class Meta:
        model = Membership
        fields = ['user__username', 'role']


class MembershipRequestFilter(django_filters.FilterSet):
    user__username = django_filters.CharFilter(lookup_expr='icontains', label='Username')

    class Meta:
        model = Membership
        fields = ['user__username']
