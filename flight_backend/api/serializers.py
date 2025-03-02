from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['flight_number', 'airline', 'origin', 'destination', 'status',
                  'aircraft', 'live_latitude', 'live_longitude']