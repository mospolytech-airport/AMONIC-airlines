from django.db import models

from country.models import Country

class Office(models.Model):
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)