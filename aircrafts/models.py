from django.db import models

# Create your models here.
class Aircraft(models.Model):
    Name = models.CharField(max_length=50)
    MakeModel = models.CharField(max_length=10, null=True, blank=True)
    TotalSeats = models.IntegerField()
    EconomySeats = models.IntegerField()
    BusinessSeats = models.IntegerField()