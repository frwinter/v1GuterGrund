from django.contrib import admin
from .models import Contact
from django.contrib.auth import get_user_model  
from users.admin import ExportCsvMixin  # Wiederverwendung des Mixins

User = get_user_model()

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ['export_as_csv']
    list_display = ('first_name', 'last_name', 'phone_masked', 'status', 'user')
    list_filter = ('status', 'user')
    search_fields = ('first_name', 'last_name', 'phone_masked')
    readonly_fields = ('phone_masked', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)