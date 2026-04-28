from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather_view, name='weather'),
    path('posts/', views.posts_view, name='posts'),
]