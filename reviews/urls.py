from django.urls import path

from . import views

app_name = 'reviews'
urlpatterns = [
  path('', views.ReviewView.as_view(), name='list'),
  # path('<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
]
