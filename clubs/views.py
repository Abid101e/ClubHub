from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django_filters.views import FilterView
from clubs.models import Club
from clubs.forms import ClubForm
from clubs.filters import ClubFilter


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
        return Club.objects.select_related('creator')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.object

        context['news_posts'] = club.posts.filter(
            type='NEWS',
            is_published=True
        ).select_related('author').order_by('-created_at')[:5]

        context['blog_posts'] = club.posts.filter(
            type='BLOG',
            is_published=True
        ).select_related('author').order_by('-created_at')[:5]

        if self.request.user.is_authenticated:
            context['user_membership'] = club.membership_set.filter(
                user=self.request.user
            ).first()
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
