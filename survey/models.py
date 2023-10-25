from django.db import models


class Survey(models.Model):
    mounth = models.DateField(verbose_name='Месяц опроса', blank=True, null=True)
    departure = models.CharField(max_length=200)
    arrival = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=200)
    cabintype = models.CharField(max_length=200)
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()
