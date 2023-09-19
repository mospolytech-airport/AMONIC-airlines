from django.db import models

class Office(models.Model):
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)