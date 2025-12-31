from django.urls import path
from django.views.generic import TemplateView


app_name = 'clubs'

urlpatterns = [
    path('', TemplateView.as_view(template_name='clubs/club_list.html'), name='list'),
    path('new/', TemplateView.as_view(template_name='clubs/club_form.html'), name='create'),
]