from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from clubs.models import Club


class ClubMemberRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        club = self.get_club()
        return club.membership_set.filter(
            user=self.request.user,
            status='APPROVED'
        ).exists()

    def get_club(self):
        return get_object_or_404(Club, pk=self.kwargs.get('pk') or self.kwargs.get('club_pk'))


class ClubAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        club = self.get_club()
        return club.membership_set.filter(
            user=self.request.user,
            role='ADMIN',
            status='APPROVED'
        ).exists()

    def get_club(self):
        return get_object_or_404(Club, pk=self.kwargs.get('pk') or self.kwargs.get('club_pk'))


class ClubModeratorOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        club = self.get_club()
        return club.membership_set.filter(
            user=self.request.user,
            role__in=['ADMIN', 'MODERATOR'],
            status='APPROVED'
        ).exists()

    def get_club(self):
        return get_object_or_404(Club, pk=self.kwargs.get('pk') or self.kwargs.get('club_pk'))
