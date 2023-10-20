from django.db import models
from schedules.models import Schedule
from cabintypes.models import CabinType
from authentication.models import User

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    cabin_type = models.ForeignKey(CabinType, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=14)
    passport_number = models.CharField(max_length=9)
    passport_country_id = models.IntegerField()
    booking_reference = models.CharField(max_length=6)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

