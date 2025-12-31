from django.urls import path
from clubs.views import ClubListView, ClubDetailView, ClubCreateView
from memberships.views import (
    JoinClubView,
    MemberListView,
    MembershipRequestListView,
    ApproveMembershipView,
    RejectMembershipView,
    PromoteMemberView,
    DemoteMemberView
)


app_name = 'clubs'

urlpatterns = [
    path('', ClubListView.as_view(), name='list'),
    path('new/', ClubCreateView.as_view(), name='create'),
    path('membership/<int:pk>/approve/', ApproveMembershipView.as_view(), name='approve_membership'),
    path('membership/<int:pk>/reject/', RejectMembershipView.as_view(), name='reject_membership'),
    path('membership/<int:pk>/promote/', PromoteMemberView.as_view(), name='promote_member'),
    path('membership/<int:pk>/demote/', DemoteMemberView.as_view(), name='demote_member'),
    path('<int:pk>/join/', JoinClubView.as_view(), name='join'),
    path('<int:pk>/members/', MemberListView.as_view(), name='members'),
    path('<int:pk>/requests/', MembershipRequestListView.as_view(), name='requests'),
    path('<slug:slug>/', ClubDetailView.as_view(), name='detail'),
]