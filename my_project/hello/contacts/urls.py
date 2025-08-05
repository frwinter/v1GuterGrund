from django.urls import path
from . import views

app_name = 'contacts'  # Optional, aber empfohlen für Namespacing


urlpatterns = [
    # Hauptansicht (Liste + Formular kombiniert)
    path('', views.contact_list, name='index'),  # Einheitlicher Name 'list'
    path('edit/<int:pk>/', views.edit_contact, name='edit'),
    path('delete/<int:pk>/', views.delete_contact, name='delete'),
    path('export/<int:pk>/', views.export_contact, name='export'),
    # Alternative falls getrennte Views gewünscht:
    # path('', views.index, name='index'),  # Nur für Startseite
    # path('list/', views.contact_list, name='list'),
    # path('add/', views.add_contact, name='add'),
]