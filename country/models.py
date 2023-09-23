from django.db import models

from office.models import Office

class Country(models.Model):
    name = models.CharField(max_length=200)
    country_id = models.ForeignKey(Office, on_delete=models.CASCADE, blank=True, null=True)