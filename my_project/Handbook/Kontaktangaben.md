📝 1. Datenbank-Modell erweitern
Öffne contacts/models.py und füge neue Felder hinzu:

python
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    # Neue Felder:
    address = models.TextField(blank=True)  # Optional
    birth_date = models.DateField(null=True, blank=True)  # Optional
    is_customer = models.BooleanField(default=False)  # Checkbox
🔄 2. Migration erstellen & anwenden
bash
python manage.py makemigrations contacts
python manage.py migrate
📋 3. Formular anpassen
In contacts/forms.py:

python
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'address', 'birth_date', 'is_customer']  # Alle Felder einbinden
        
    # Optional: Custom Widget für bessere Darstellung
    widgets = {
        'birth_date': forms.DateInput(attrs={'type': 'date'}),  # Date-Picker
    }
🎨 4. Template aktualisieren
In contacts/templates/contacts/add.html:

html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}  <!-- Zeigt automatisch alle Felder an -->
    <button type="submit" class="btn btn-primary">Speichern</button>
</form>

<!-- ODER manuell für bessere Kontrolle: -->
<form method="post">
    {% csrf_token %}
    <div class="mb-3">
        <label class="form-label">Adresse</label>
        {{ form.address }}
    </div>
    <div class="mb-3">
        <label class="form-label">Geburtsdatum</label>
        {{ form.birth_date }}
    </div>
    <div class="mb-3 form-check">
        {{ form.is_customer }}
        <label class="form-check-label">Ist Kunde?</label>
    </div>
    <!-- ... -->
</form>
✅ 5. Admin-Oberfläche anpassen
In contacts/admin.py:

python
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_customer')  # Neue Felder in der Übersicht
    list_filter = ('is_customer',)  # Filter-Sidebar
🔍 6. Ergebnis prüfen
Server starten:

bash
python manage.py runserver
Testen unter:

Formular: http://localhost:8000/contacts/neu/

Admin: http://localhost:8000/admin/contacts/contact/

💡 Tipps für spezielle Feldtypen
Auswahlfelder:

python
STATUS_CHOICES = [('new', 'Neu'), ('active', 'Aktiv')]
status = models.CharField(max_length=10, choices=STATUS_CHOICES)
Bilder:

python
avatar = models.ImageField(upload_to='avatars/', blank=True)
(Vergiss nicht pillow zu installieren: pip install pillow)