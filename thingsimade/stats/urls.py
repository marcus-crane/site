from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'stats'
urlpatterns = [
    path('', TemplateView.as_view(template_name='stats/index.html'), name='index'),
    path('lastfm/', views.lastfm, name='lastfm')
]