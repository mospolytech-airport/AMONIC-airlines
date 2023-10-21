from rest_framework import viewsets

from aircrafts.models import Aircraft
from aircrafts.serializers import AircraftSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()
