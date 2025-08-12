from rest_framework import serializers
from ..models import Event

class EventSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='event_type.name')
    type_color = serializers.CharField(source='event_type.color')
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'type_name', 'type_color',
            'start', 'end', 'location', 'online_link'
        ]