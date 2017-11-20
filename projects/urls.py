from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
  path('', views.ProjectView.as_view(), name='list'),
  path('<slug:slug>/', views.ProjectDetailView.as_view(), name='detail'),
]