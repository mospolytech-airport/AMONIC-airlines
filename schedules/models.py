from django.db import models
from aircrafts.models import Aircraft
from airoutes.models import Route


class Schedule(models.Model):
    Date = models.DateField()
    Time = models.TimeField()
    Aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    Route = models.ForeignKey(Route, on_delete=models.CASCADE)
    EconomyPrice = models.DecimalField(max_digits=10, decimal_places=2)
    Confirmed = models.BooleanField()
    FlightNumber = models.CharField(max_length=10, null=True, blank=True)
