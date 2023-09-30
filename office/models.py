from django.db import models

from country.models import Country

class Office(models.Model):
    title = models.CharField(max_length=100)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
