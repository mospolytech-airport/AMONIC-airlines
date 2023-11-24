from rest_framework import serializers

from schedules.models import Schedule
from aircrafts.models import Aircraft
from airports.models import Airport
from airoutes.models import Route
from aircrafts.serializers import AircraftSerializer
from airoutes.serializers import RouteSerializer

from django.utils.dateparse import parse_date


class ScheduleSerializer(serializers.ModelSerializer):
    Aircraft = AircraftSerializer()
    Route = RouteSerializer()
    
    class Meta:
        model = Schedule
        fields = '__all__'
    
    def create(self, validated_data):
        aircraft_data = validated_data.pop('Aircraft')
        route_data = validated_data.pop('Route')

        aircraft = Aircraft.objects.create(**aircraft_data)
        departure_airport_data = route_data.pop('DepartureAirport')
        arrival_airport_data = route_data.pop('ArrivalAirport')
        
        departure_airport = Airport.objects.create(**departure_airport_data)
        arrival_airport = Airport.objects.create(**arrival_airport_data)

        route = Route.objects.create(DepartureAirport=departure_airport, ArrivalAirport=arrival_airport, **route_data)
        
        schedule = Schedule.objects.create(Aircraft=aircraft, Route=route, **validated_data)
        return schedule
    
    def update(self, instance, validated_data):
        try:
            Confirmed = validated_data.pop('Confirmed')
            Aircraft = validated_data.pop('Aircraft')
            Route = validated_data.pop('Route')
            Date = validated_data.pop('Date')
            Time = validated_data.pop('Time')
            EconomyPrice = validated_data.pop('EconomyPrice')
            FlightNumber = validated_data.pop('FlightNumber')

            instance.Confirmed = bool(Confirmed)
            instance.Aircraft_id = Aircraft["id"]
            instance.Route_id = Route["id"]
            instance.Date = Date
            instance.EconomyPrice = EconomyPrice 
            instance.FlightNumber = FlightNumber 
            instance.Time = Time
            instance.save()

            return instance

        except Exception as e:
            print(f"Error in update: {e}")
            raise
