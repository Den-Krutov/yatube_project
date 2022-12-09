from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('group/<slug:slug_str>/', views.group_posts),
]
