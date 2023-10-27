from rest_framework import serializers

from schedules.models import Schedule
from aircrafts.serializers import AircraftSerializer
from airoutes.serializers import RouteSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    Aircraft = AircraftSerializer()
    Route = RouteSerializer()
    
    class Meta:
        model = Schedule
        fields = '__all__'
