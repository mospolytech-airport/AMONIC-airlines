from rest_framework import viewsets

from amenitiesTickets.models import AmenityTicket
from amenitiesTickets.serializers import AmenityTicketSerializer


class AmenityTicketViewSet(viewsets.ModelViewSet):
    serializer_class = AmenityTicketSerializer
    queryset = AmenityTicket.objects.all()
