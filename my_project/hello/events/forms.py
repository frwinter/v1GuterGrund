from django import forms
from .models import EventRegistration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['name', 'email', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

class SimpleRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    accept_terms = forms.BooleanField(required=True)