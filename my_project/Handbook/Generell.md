1. Felder anpassen
markdown
### Neue Kontaktfelder hinzufügen  
1. In `contacts/models.py` Feld definieren:  
   ```python  
   new_field = models.CharField(max_length=100, blank=True)  
Migration erstellen:

bash
python manage.py makemigrations contacts  
python manage.py migrate  
In contacts/forms.py Feld zur Liste hinzufügen:

python
fields = [..., 'new_field']  
text

#### **2. Formular-Layout anpassen**  
```markdown
### Formularfelder gruppieren  
In `add.html` Felder manuell anordnen:  
```html  
<div class="section">  
    <h3>Basisdaten</h3>  
    {{ form.name }}  
    {{ form.email }}  
</div>  
text

#### **3. Wichtige Dateien**  
```markdown
- `models.py` → Datenbankfelder  
- `forms.py` → Formularlogik  
- `admin.py` → Admin-Oberfläche  
- `templates/contacts/add.html` → Frontend  
4. Troubleshooting
markdown
### Häufige Fehler  
- **"Tabelle existiert nicht"**:  
  ```bash  
  rm -f db.sqlite3 && python manage.py migrate  
Feld erscheint nicht:

Prüfe fields-Liste in forms.py

Server neu starten!

text

#### **5. Best Practices**  
```markdown
- Für optionale Felder immer `blank=True` setzen  
- Boolesche Felder: `BooleanField(default=False)`  
- Sensible Daten: `null=True, blank=True` (z.B. Geburtsdatum)  
🌟 Bonus: Screenshots einfügen
Admin-Oberfläche mit neuen Feldern

Formular-Frontend

Beispiel-Migration

🔗 Nützliche Links
markdown
- [Django Model Field Reference](https://docs.djangoproject.com/en/5.2/ref/models/fields/)  
- [Formular-Widgets](https://docs.djangoproject.com/en/5.2/ref/forms/widgets/)  
🚀 Fertig! Mit dieser Dokumentation können andere Orgas:
✅ Felder selbst anpassen
✅ Probleme lösen
✅ Konsistente Strukturen beibehalten