from django.contrib import admin
from .models import Event, EventType
from users.admin import ExportCsvMixin  # Wiederverwendung des Mixins


@admin.register(Event)
class EventAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ['export_as_csv']
    list_display = ('title', 'event_type', 'start', 'responsible')

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    