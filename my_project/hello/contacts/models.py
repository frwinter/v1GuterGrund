from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.conf import settings  # Wichtig: Diesen Import hinzufügen


class Contact(models.Model):
    STATUS_CHOICES = [
        ('active', 'Aktiv'),
        ('left', 'Ist raus'),
        ('needs_info', 'Braucht Infos'),
        ('inactive', 'Inaktiv'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Benutzer"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_raw = models.CharField(max_length=20, verbose_name="Telefonnummer (voll)")
    signal_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validierung für entweder Telefon oder Signal
        if not self.phone_raw and not self.signal_id:
            raise ValidationError("Mindestens Telefon oder Signal ID muss angegeben werden")
    @property
    def phone_masked(self):
        if self.phone_raw:
            return f"{self.phone_raw[:2]}...{self.phone_raw[-3:]}"
        return ""

    # phone_masked = models.CharField(max_length=5, editable=False)  # LÖSCHEN!

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        app_label = 'contacts'  # ← DIESE ZEILE EINFÜGEN
        unique_together = ['user', 'first_name', 'last_name', 'phone_raw']
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontakte"
