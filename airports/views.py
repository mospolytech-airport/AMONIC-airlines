from rest_framework import viewsets

from airports.models import Airport
from airports.serializers import AirportSerializer


class AirportViewSet(viewsets.ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
