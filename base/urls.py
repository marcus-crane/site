from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'base'
urlpatterns = [
  path('', TemplateView.as_view(template_name='base/index.html')),
]