from django.views.generic import ListView, CreateView, DetailView, TemplateView
from .forms import RegistrationForm, SimpleRegistrationForm # Falls du ein Formular brauchst
from .models import Event, EventType
from django.shortcuts import redirect, render, get_object_or_404  # WICHTIG: Diesen Import hinzufügen
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['form'] = SimpleRegistrationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if request.user.is_authenticated:
            # Bestehende Logik für angemeldete User
            return self.handle_authenticated_user(request)
        
        # Logik für nicht angemeldete User
        form = SimpleRegistrationForm(request.POST)
        if form.is_valid():
            return self.handle_anonymous_registration(form)
        
        return self.render_to_response(self.get_context_data(form=form))
    
    def handle_anonymous_registration(self, form):
        # Hier die Registrierungslogik für nicht angemeldete User
        # z.B. Email versenden, Daten speichern etc.
        messages.success(self.request, "Anmeldung erfolgreich")
        return redirect('events:registration_success')

class CalendarBaseView(TemplateView):
    template_name = 'events/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all().select_related('event_type')
        context['event_types'] = EventType.objects.all()
        return context

class YearView(CalendarBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'year'
        return context

class MonthView(CalendarBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'month'
        return context

class WeekView(CalendarBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'week'
        return context

class DayView(CalendarBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'day'
        return context

class ListView(CalendarBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'list'
        return context 

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter nach Eventtypen wenn Parameter vorhanden
        event_types = self.request.GET.getlist('types')
        if event_types:
            queryset = queryset.filter(event_type__id__in=event_types)
        return queryset.order_by('start')

def event_filter(request):
    event_type = request.GET.get('type')
    view_type = request.GET.get('view')
    
    events = Event.objects.all()
    if event_type:
        events = events.filter(event_type__id=event_type)
    
    if view_type == 'json':
        data = [{
            'title': e.title,
            'start': e.start.isoformat(),
            'end': e.end.isoformat(),
            'color': e.event_type.color,
            'url': reverse('events:event_detail', kwargs={'pk': e.pk})
        } for e in events]
        return JsonResponse(data, safe=False)
    
    return render(request, 'events/partials/event_list.html', {'events': events})
