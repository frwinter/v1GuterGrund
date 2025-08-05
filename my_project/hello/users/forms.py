from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Max'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Mustermann'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'max@example.com'})
    )
    password1 = forms.CharField(
        label="Passwort",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mindestens 8 Zeichen'}),
        help_text="Mindestens 8 Zeichen, nicht nur Zahlen"
    )
    password2 = forms.CharField(
        label="Passwort bestätigen",
        widget=forms.PasswordInput(attrs={'placeholder': 'Passwort wiederholen'}),
        strip=False,
        help_text="Geben Sie das gleiche Passwort wie oben ein"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Diese E-Mail-Adresse ist bereits registriert")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1, self.instance)
        except ValidationError as e:
            raise ValidationError('\n'.join(e.messages))  # Kombiniert alle Fehlermeldungen
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Die Passwörter stimmen nicht überein")

        return cleaned_data