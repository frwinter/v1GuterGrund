from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Registration

@receiver(post_save, sender=Registration)
def send_confirmation(sender, instance, created, **kwargs):
    if created:
        send_mail(
            instance.event.confirmation_email_subject,
            instance.event.confirmation_email_body,
            'noreply@example.com',
            [instance.email],
            fail_silently=False,
        )