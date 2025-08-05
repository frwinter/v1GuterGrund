from django.views.generic import ListView, CreateView, DetailView
from .forms import RegistrationForm, SimpleRegistrationForm # Falls du ein Formular brauchst
from .models import Event
from django.shortcuts import redirect, render  # WICHTIG: Diesen Import hinzufügen
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

def registration_success_view(request):
    return render(request, 'events/registration_success.html', {
        'message': 'Deine Anmeldung war erfolgreich!'
    })
def get_object(self, queryset=None):
    try:
        return super().get_object(queryset)
    except Http404:
        # Custom Fehlerbehandlung hier
        raise Http404("Dieses Event existiert nicht")
    
class CalendarView(ListView):
    model = Event
    template_name = 'events/calendar.html'
    context_object_name = 'events'

class EventCreateView(CreateView):
    model = Event
    fields = '__all__'
    success_url = '/calendar/'

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    login_url = '/login/'  # Falls nicht eingeloggt


    def get(self, request, *args, **kwargs):
        # Sicherstellen, dass self.object gesetzt ist
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Automatische Anmeldung für eingeloggte User
        if request.user.is_authenticated:
            try:
                # Prüfen, ob bereits angemeldet
                if not self.object.participants.filter(id=request.user.id).exists():
                    self.object.participants.add(request.user)
                    messages.success(request, "Erfolgreich angemeldet!")
                else:
                    messages.info(request, "Du bist bereits angemeldet.")
                return redirect('events:event_detail', pk=self.object.pk)
            
            except Exception as e:
                messages.error(request, f"Fehler: {str(e)}")
                return self.render_to_response(self.get_context_data())
        
        # Fallback für nicht eingeloggt (zeigt Formular)
        return super().post(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        # Sicherstellen, dass self.object vorhanden ist
        context = super().get_context_data(**kwargs)
        if 'form' not in kwargs:
            context['form'] = SimpleRegistrationForm()
        return context


def index(request):
    return render(request, 'events/index.html')