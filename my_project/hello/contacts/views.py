from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .forms import ContactForm  # Stelle sicher, dass du forms.py erstellt hast
from django.contrib.auth.decorators import login_required  
from django.db.models import Q  # WICHTIG: Diesen Import hinzufügen
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()  # Holt das korrekte User-Modell    


@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user).prefetch_related('user')
    
    # Vorbereitung der ähnlichen Kontakte
    contact_matches = {}
    for contact in contacts:
        # Finde Kontakte mit gleichem Vor- und Nachnamen (case-insensitive)
        similar = Contact.objects.exclude(user=request.user).filter(
            Q(first_name__iexact=contact.first_name) &
            Q(last_name__iexact=contact.last_name) &
            (
                Q(phone_raw__endswith=contact.phone_raw[-3:]) if contact.phone_raw else Q() |
                Q(signal_id__iexact=contact.signal_id) if contact.signal_id else Q()
            )
        ).distinct()
        ##Das ist die einfachere Logik 
        #similar = Contact.objects.exclude(user=request.user).filter(
        #    Q(first_name__iexact=contact.first_name) &
        #    Q(last_name__iexact=contact.last_name)
        #).select_related('user')
        
        if similar.exists():
            contact_matches[contact.id] = similar

    if request.method == 'POST':
        if 'save_all' in request.POST:
            for contact in contacts:
                contact.first_name = request.POST.get(f'first_name_{contact.id}', contact.first_name)
                contact.last_name = request.POST.get(f'last_name_{contact.id}', contact.last_name)
                contact.phone_raw = request.POST.get(f'phone_raw_{contact.id}', contact.phone_raw)
                contact.signal_id = request.POST.get(f'signal_id_{contact.id}', contact.signal_id)
                contact.status = request.POST.get(f'status_{contact.id}', contact.status)
                contact.save()
            messages.success(request, "Alle Änderungen gespeichert!")
            return redirect('contacts:index')
        
        elif 'add_new' in request.POST:
            Contact.objects.create(
                user=request.user,
                first_name=request.POST.get('new_first_name', ''),
                last_name=request.POST.get('new_last_name', ''),
                phone_raw=request.POST.get('new_phone_raw', ''),
                signal_id=request.POST.get('new_signal_id', ''),
                status=request.POST.get('new_status', 'active')
            )
            messages.success(request, "Neuer Kontakt hinzugefügt!")
            return redirect('contacts:index')
    
    return render(request, 'contacts/list.html', {
        'contacts': contacts,
        'contact_matches': contact_matches,
        'STATUS_CHOICES': Contact.STATUS_CHOICES
    })

@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    # Bearbeitungslogik hier


@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    
    if request.method == 'POST':  # Sicherer mit POST
        contact.delete()
        messages.success(request, "Kontakt wurde gelöscht!")
        return redirect('contacts:index')
    
    # Falls GET (z.B. direkter Link-Klick)
    messages.error(request, "Kontakt konnte nicht gelöscht werden!")
    return redirect('contacts:index')

@login_required 
def export_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    # Exportlogik hier

def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kontakt wurde gespeichert!")


## DAS IST NOCH AUS DEM ALTEN CONTACT DING 
#def add_contact(request):
#    """Handhabt das Formular für neue Kontakte"""
#    if request.method == 'POST':
#        form = ContactForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('contact_list')  # Zurück zur Liste nach Speichern
#    else:
#        form = ContactForm()  # Leeres Formular für GET-Requests
#    
#    return render(request, 'contacts/add.html', {'form': form})
#
#
#def index(request):
#    return render(request, 'contacts/index.html')