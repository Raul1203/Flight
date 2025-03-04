from rest_framework import serializers
from .models import Flight, AircraftWithMostFlights, DayWithMostFlights, MostVisitedDestination,AirplaneLocation

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['flight_number', 'airline', 'origin', 'destination', 'status',
                  'aircraft', 'live_latitude', 'live_longitude']
        
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftWithMostFlights
        fields = ['month', 'aircraft', 'flight_count']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneLocation
        fields = ['latitude', 'longitude']

class MostFlightSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many = True, read_only = True)

    class Meta:
        model = DayWithMostFlights
        fields = ['month', 'day', 'flight_count', 'location']


class TopDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MostVisitedDestination
        fields = ['month', 'destianation', 'visit_count']