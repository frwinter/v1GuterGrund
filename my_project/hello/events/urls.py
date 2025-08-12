from django.urls import path
from . import views  # WICHTIG: Diesen Import hinzufügen
from .views import CalendarView, EventDetailView, DayView, WeekView, MonthView, YearView, ListView, event_filter
from .embed import EmbedView
from django.contrib.auth import views as auth_views

app_name = 'events'  # Optional, aber empfohlen für Namespacing


urlpatterns = [
#    path('', views.index, name='index'),  # Dies erstellt 'events:index'
    path('', CalendarView.as_view(), name='calendar'),
    path('day/', DayView.as_view(), name='day_view'),
    path('week/', WeekView.as_view(), name='week_view'),
    path('month/', MonthView.as_view(), name='month_view'),
    path('year/', YearView.as_view(), name='year_view'),
    path('list/', ListView.as_view(), name='list_view'),
    path('filter/', event_filter, name='event_filter'),
    path('embed/', EmbedView.as_view(), name='embed'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),  # Neu
    path('registration/success/', views.registration_success_view, name='registration_success'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]