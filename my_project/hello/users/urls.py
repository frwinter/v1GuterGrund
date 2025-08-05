from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from .views import register_view  # Wichtig: Import der View-Funktion


app_name = 'users'

urlpatterns = [
    path('', views.register_view, name='register'),  # POST/GET für Registrierung
    path('activate/<str:token>/', views.activate_account, name='activate'),
    path('registration/complete/', views.registration_complete, name='registration_complete'),
    path('resend-activation/', views.resend_activation, name='resend_activation'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True  # Eingeloggte User werden zu dashboard umgeleitet
    ), name='login'),    
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/login/'
    ), name='logout'),
]