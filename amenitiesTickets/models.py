from django.db import models
from tickets.models import Ticket
from amenities.models import Amenity

class AmenityTicket(models.Model):
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=4, default=0.0000)

    class Meta:
        unique_together = ('amenity', 'ticket')
