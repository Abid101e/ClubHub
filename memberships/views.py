from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from clubs.models import Club
from clubs.mixins import ClubMemberRequiredMixin, ClubAdminRequiredMixin
from memberships.models import Membership


class JoinClubView(LoginRequiredMixin, View):
    def post(self, request, pk):
        club = get_object_or_404(Club, pk=pk)

        existing_membership = Membership.objects.filter(
            user=request.user,
            club=club
        ).first()

        if existing_membership:
            if existing_membership.status == 'PENDING':
                messages.info(request, 'Your membership request is already pending.')
            elif existing_membership.status == 'APPROVED':
                messages.warning(request, 'You are already a member of this club.')
            elif existing_membership.status == 'REJECTED':
                messages.error(request, 'Your previous membership request was rejected.')
        else:
            Membership.objects.create(
                user=request.user,
                club=club,
                status='PENDING'
            )
            messages.success(request, f'Your request to join "{club.name}" has been submitted!')

        return redirect('clubs:detail', slug=club.slug)


class MemberListView(LoginRequiredMixin, ClubMemberRequiredMixin, ListView):
    model = Membership
    template_name = 'clubs/member_list.html'
    context_object_name = 'members'

    def get_queryset(self):
        club = self.get_club()
        return Membership.objects.filter(
            club=club,
            status='APPROVED'
        ).select_related('user').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.get_club()
        if self.request.user.is_authenticated:
            context['user_membership'] = self.get_club().membership_set.filter(
                user=self.request.user,
                status='APPROVED'
            ).first()
        return context


class MembershipRequestListView(LoginRequiredMixin, ClubAdminRequiredMixin, ListView):
    model = Membership
    template_name = 'clubs/membership_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        club = self.get_club()
        return Membership.objects.filter(
            club=club,
            status='PENDING'
        ).select_related('user').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.get_club()
        return context


class ApproveMembershipView(LoginRequiredMixin, ClubAdminRequiredMixin, View):
    def get_club(self):
        membership = get_object_or_404(Membership, pk=self.kwargs['pk'])
        return membership.club

    def post(self, request, pk):
        membership = get_object_or_404(Membership, pk=pk)
        club = membership.club

        if membership.status == 'PENDING':
            membership.status = 'APPROVED'
            membership.save()
            messages.success(request, f'{membership.user.username} has been approved as a member!')
        else:
            messages.warning(request, 'This membership request has already been processed.')

        return redirect('clubs:requests', pk=club.pk)


class RejectMembershipView(LoginRequiredMixin, ClubAdminRequiredMixin, View):
    def get_club(self):
        membership = get_object_or_404(Membership, pk=self.kwargs['pk'])
        return membership.club

    def post(self, request, pk):
        membership = get_object_or_404(Membership, pk=pk)
        club = membership.club

        if membership.status == 'PENDING':
            membership.status = 'REJECTED'
            membership.save()
            messages.success(request, f'{membership.user.username}\'s request has been rejected.')
        else:
            messages.warning(request, 'This membership request has already been processed.')

        return redirect('clubs:requests', pk=club.pk)


class PromoteMemberView(LoginRequiredMixin, ClubAdminRequiredMixin, View):
    def get_club(self):
        membership = get_object_or_404(Membership, pk=self.kwargs['pk'])
        return membership.club

    def post(self, request, pk):
        membership = get_object_or_404(Membership, pk=pk)
        club = membership.club

        if membership.role == 'ADMIN':
            messages.warning(request, 'Cannot change role of club admin.')
        elif membership.status != 'APPROVED':
            messages.error(request, 'Can only promote approved members.')
        else:
            membership.role = 'MODERATOR'
            membership.save()
            messages.success(request, f'{membership.user.username} has been promoted to Moderator!')

        return redirect('clubs:members', pk=club.pk)


class DemoteMemberView(LoginRequiredMixin, ClubAdminRequiredMixin, View):
    def get_club(self):
        membership = get_object_or_404(Membership, pk=self.kwargs['pk'])
        return membership.club

    def post(self, request, pk):
        membership = get_object_or_404(Membership, pk=pk)
        club = membership.club

        if membership.role == 'ADMIN':
            messages.warning(request, 'Cannot change role of club admin.')
        elif membership.status != 'APPROVED':
            messages.error(request, 'Can only demote approved members.')
        else:
            membership.role = 'MEMBER'
            membership.save()
            messages.success(request, f'{membership.user.username} has been demoted to Member.')

        return redirect('clubs:members', pk=club.pk)
