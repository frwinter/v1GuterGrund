"""
URL configuration for hello project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import dashboard  # Eigenes Dashboard-View
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('login')),

    path('admin/', admin.site.urls),
    
    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', include('users.urls')),  # Registrierung (s. Schritt 3)
    
    # Apps
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard nach Login
    path('events/', include('events.urls', namespace='events')),  # Events-App
    path('contacts/', include('contacts.urls', namespace='contacts')),  # Kontakte-App
    
    # Root-URL: Weiterleitung zu login/dashboard
    path('', lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('login')),
]
