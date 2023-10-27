from rest_framework import serializers

from airoutes.models import Route
from airports.serializers import AirportSerializer


class RouteSerializer(serializers.ModelSerializer):
    DepartureAirport = AirportSerializer()
    ArrivalAirport = AirportSerializer()
    
    class Meta:
        model = Route
        fields = '__all__'
