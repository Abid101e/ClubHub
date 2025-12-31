from django.urls import path
from posts.views import PostCreateView


app_name = 'posts'

urlpatterns = [
    path('clubs/<int:club_pk>/posts/new/', PostCreateView.as_view(), name='create'),
]
