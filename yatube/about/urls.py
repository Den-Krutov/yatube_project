from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('author/', views.AboutAuthorPageView.as_view(), name='author'),
    path('tech/', views.AboutTechPageView.as_view(), name='tech'),
]
