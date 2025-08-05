# events/api/views.py
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

class EventListAPI(generics.ListAPIView):
    queryset = Event.objects.filter(is_public=True)
    serializer_class = EventSerializer