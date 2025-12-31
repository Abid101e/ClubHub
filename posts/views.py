from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from clubs.models import Club
from clubs.mixins import ClubMemberRequiredMixin
from posts.models import Post
from posts.forms import PostForm
from memberships.models import Membership


class PostCreateView(LoginRequiredMixin, ClubMemberRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def get_club(self):
        return get_object_or_404(Club, pk=self.kwargs['club_pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        club = self.get_club()
        membership = Membership.objects.approved().for_club(club).filter(
            user=self.request.user
        ).first()
        kwargs['user_role'] = membership.role if membership else None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.get_club()
        return context

    def form_valid(self, form):
        club = self.get_club()
        membership = Membership.objects.approved().for_club(club).filter(
            user=self.request.user
        ).first()

        if not membership:
            messages.error(self.request, 'You must be a member to create posts.')
            return redirect('clubs:detail', slug=club.slug)

        form.instance.club = club
        form.instance.author = self.request.user

        if form.instance.type == 'NEWS' and membership.role not in ['ADMIN', 'MODERATOR']:
            messages.error(self.request, 'Only admins and moderators can create news posts.')
            return redirect('clubs:detail', slug=club.slug)

        messages.success(self.request, f'Post "{form.instance.title}" created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clubs:detail', kwargs={'slug': self.get_club().slug})


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.published().select_related('club', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.object.club
        if self.request.user.is_authenticated:
            context['user_membership'] = Membership.objects.approved().for_club(
                self.object.club
            ).filter(user=self.request.user).first()
        return context
