from rest_framework import viewsets

from tickets.models import Ticket
from tickets.serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
