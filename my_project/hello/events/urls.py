from django.urls import path
from . import views  # WICHTIG: Diesen Import hinzufügen
from .views import CalendarView, EventDetailView
from django.contrib.auth import views as auth_views

app_name = 'events'  # Optional, aber empfohlen für Namespacing


urlpatterns = [
    path('', views.index, name='index'),  # Dies erstellt 'events:index'
    path('', CalendarView.as_view(), name='calendar'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),  # Neu
    path('registration/success/', views.registration_success_view, name='registration_success'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]