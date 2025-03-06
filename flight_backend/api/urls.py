from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, AircraftViewSet, MostFlightViewSet, TopDestinationViewSet, AirportWithMostDeparturesViewSet

router = DefaultRouter()

router.register('flights', FlightViewSet, basename='flight')
router.register('aircraft', AircraftViewSet)
router.register('most-flights', MostFlightViewSet)
router.register('top-destination', TopDestinationViewSet)
router.register('airport-departures', AirportWithMostDeparturesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]