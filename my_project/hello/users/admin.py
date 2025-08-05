from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import User 

User = get_user_model()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"
    
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('username', 'email', 'active_status', 'date_joined')
    list_filter = ('is_active', 'is_superuser')
    search_fields = ('username', 'email')
    actions = ["export_as_csv"]

    def active_status(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.is_active else 'red',
            'Aktiv' if obj.is_active else 'Inaktiv'
        )
    active_status.short_description = 'Status'



