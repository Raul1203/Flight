from rest_framework import viewsets
from .models import Flight, AircraftWithMostFlights, DayWithMostFlights, MostVisitedDestination, AirportWithMostDepartures
from .serializers import (
    FlightSerializer, 
    AircraftSerializer, 
    MostFlightSerializer, 
    TopDestinationSerializer,
    AirportWithMostDeparturesSerializer
)

class FlightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class AircraftViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AircraftWithMostFlights.objects.all().order_by('-month')
    serializer_class = AircraftSerializer

class MostFlightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DayWithMostFlights.objects.all().order_by('-month').prefetch_related('locations')
    serializer_class = MostFlightSerializer

class TopDestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MostVisitedDestination.objects.all().order_by('-month')
    serializer_class = TopDestinationSerializer

class AirportWithMostDeparturesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AirportWithMostDepartures.objects.all().order_by('-month')
    serializer_class = AirportWithMostDeparturesSerializer