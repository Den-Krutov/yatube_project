from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from . import views

app_name = 'users'

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('signup/', views.SingUp.as_view(), name='signup'),
    path('password_change/',
         PasswordChangeView.as_view(template_name='users/'
                                                  'password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         PasswordChangeDoneView
         .as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         PasswordResetView
         .as_view(template_name='users/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView
         .as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView
         .as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confim'),
    path('reset/done/',
         PasswordResetCompleteView
         .as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
