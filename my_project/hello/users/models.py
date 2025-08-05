from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)

activation_token_generator = AccountActivationTokenGenerator()

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=40, blank=True)
    activation_token_created = models.DateTimeField(null=True, blank=True)
    
    def is_activation_token_valid(self):
        if not self.activation_token_created:
            return False
        return (timezone.now() - self.activation_token_created).total_seconds() < 86400  # 24 Stunden
        
    def generate_activation_token(self):
        self.activation_token = get_random_string(40)
        self.activation_token_created = timezone.now()
        self.save()