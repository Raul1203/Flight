from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Flight
from .serializers import FlightSerializer

class FlightViewSet(ReadOnlyModelViewSet):  
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
