from rest_framework import serializers

from amenitiesTickets.models import AmenityTicket


class AmenityTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityTicket
        fields = '__all__'
