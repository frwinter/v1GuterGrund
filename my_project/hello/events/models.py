from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse


User = get_user_model()

class EventType(models.Model):
    class Meta:
        app_label = 'events'  # Explizite Zuordnung
    name = models.CharField(max_length=50)  # z.B. "Workshop", "Meeting"
    color = models.CharField(max_length=7, default='#007bff')  # Hex-Farbe

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.TextField(blank=True)
    online_link = models.URLField(blank=True)
    responsible = models.ForeignKey(User, on_delete=models.PROTECT)
    registration_form = models.TextField(blank=True)  # Oder eigenes Formular-Modell
    is_registration_open = models.BooleanField(default=True)
    participants = models.ManyToManyField(
        get_user_model(),
        related_name='events_attending',
        blank=True
    )    
    # Automatische Emails
    confirmation_email_subject = models.CharField(max_length=200)
    confirmation_email_body = models.TextField()

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})



class EventEditorRole(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    allowed_event_types = models.ManyToManyField(EventType)


class RegistrationFormField(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50, choices=[
        ('text', 'Text'),
        ('checkbox', 'Checkbox'),
        ('select', 'Auswahlmenü')
    ])
    required = models.BooleanField(default=True)

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comments = models.TextField(blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)