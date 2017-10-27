from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'projects'
urlpatterns = [
  path('', views.project_list),
]