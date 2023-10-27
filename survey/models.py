from datetime import datetime
from django.db import models


class Survey(models.Model):
    month = models.DateField(verbose_name='Месяц опроса', blank=True, null=True)
    departure = models.CharField(max_length=200)
    arrival = models.CharField(max_length=200)
    age = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=200)
    cabintype = models.CharField(max_length=200)
    q1 = models.CharField(max_length=200,blank=True, null=True)
    q2 = models.CharField(max_length=200,blank=True, null=True)
    q3 = models.CharField(max_length=200,blank=True, null=True)
    q4 = models.CharField(max_length=200,blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.month_str:  # Предполагается, что у вас есть поле month_str для хранения строки даты
            self.month = datetime.strptime(self.month_str, '%d.%m.%Y').date()
        super(Survey, self).save(*args, **kwargs)
