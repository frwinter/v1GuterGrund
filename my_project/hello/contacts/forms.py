from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_raw', 'signal_id', 'status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notizen zum Kontakt...'
            }),
        }
        labels = {
            'phone_raw': 'Telefonnummer (vollständig)',
            'signal_id': 'Signal ID',
            'first_name': 'Vorname',
            'last_name': 'Nachname',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
    # Optional: Validierungen hinzufügen
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not "@" in email:
            raise forms.ValidationError("Ungültige E-Mail-Adresse")
        return email

    def clean_signal_id(self):
        signal_id = self.cleaned_data.get('signal_id')
        if signal_id and not signal_id.startswith('@'):
            raise forms.ValidationError("Signal-ID muss mit @ beginnen.")
        return signal_id