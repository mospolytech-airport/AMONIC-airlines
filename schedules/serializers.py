from rest_framework import serializers

from schedules.models import Schedule
from aircrafts.models import Aircraft
from airports.models import Airport
from airoutes.models import Route
from aircrafts.serializers import AircraftSerializer
from airoutes.serializers import RouteSerializer


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
        # Update Aircraft data if provided
        aircraft_data = validated_data.pop('Aircraft', None)
        # print(instance., aircraft_data)
        if aircraft_data:
            aircraft_instance = instance.Aircraft
            for attr, value in aircraft_data.items():
                setattr(aircraft_instance, attr, value)
            aircraft_instance.save()

        # Update Route data if provided
        route_data = validated_data.pop('Route', None)
        if route_data:
            route_instance = instance.Route
            for attr, value in route_data.items():
                if attr in ['DepartureAirport', 'ArrivalAirport']:
                    # Handle Airport data
                    airport_instance = getattr(route_instance, attr)
                    
                    if airport_instance is None:
                        # If the airport instance doesn't exist, create a new one
                        airport_instance = Airport.objects.create(**value)
                        setattr(route_instance, attr, airport_instance)
                    else:
                        # If the airport instance exists, update its attributes
                        for airport_attr, airport_value in value.items():
                            setattr(airport_instance, airport_attr, airport_value)
                        airport_instance.save()
                else:
                    setattr(route_instance, attr, value)
            route_instance.save()

        # Update Schedule data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
    def save(self, **kwargs):
        instance = super().save(**kwargs)
        return instance