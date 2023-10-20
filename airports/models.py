from django.db import models
from country.models import Country

# Create your models here.
class Airport(models.Model):
    CountryID = models.ForeignKey(Country, on_delete=models.CASCADE)
    IATACode = models.CharField(max_length=3)
    Name = models.CharField(max_length=50)