from django.db import models
from airports.models import Airport


class Route(models.Model):
    DepartureAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_routes')
    ArrivalAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_routes')
    Distance = models.IntegerField()
    FlightTime = models.IntegerField()
