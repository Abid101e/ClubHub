from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.db.models import Prefetch
from django_filters.views import FilterView
from clubs.models import Club
from clubs.forms import ClubForm
from clubs.filters import ClubFilter
from posts.models import Post
from memberships.models import Membership


class ClubListView(FilterView):
    model = Club
    filterset_class = ClubFilter
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'
    paginate_by = 12

    def get_queryset(self):
        return Club.objects.with_member_counts().select_related('creator')


class ClubDetailView(DetailView):
    model = Club
    template_name = 'clubs/club_detail.html'
    context_object_name = 'club'

    def get_queryset(self):
        return Club.objects.select_related('creator').prefetch_related(
            Prefetch(
                'posts',
                queryset=Post.objects.select_related('author').filter(
                    is_published=True
                ).order_by('-created_at')
            ),
            Prefetch(
                'membership_set',
                queryset=Membership.objects.select_related('user').filter(
                    status='APPROVED'
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.object

        posts = list(club.posts.all())
        context['news_posts'] = [p for p in posts if p.type == 'NEWS'][:5]
        context['blog_posts'] = [p for p in posts if p.type == 'BLOG'][:5]

        if self.request.user.is_authenticated:
            context['user_membership'] = next(
                (m for m in club.membership_set.all() if m.user == self.request.user),
                None
            )
        else:
            context['user_membership'] = None

        return context


class ClubCreateView(LoginRequiredMixin, CreateView):
    model = Club
    form_class = ClubForm
    template_name = 'clubs/club_form.html'
    success_url = reverse_lazy('clubs:list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, f'Club "{form.instance.name}" created successfully!')
        return super().form_valid(form)
