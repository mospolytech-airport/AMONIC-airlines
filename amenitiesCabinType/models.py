from django.db import models
from cabintypes.models import CabinType
from amenities.models import Amenity

class CabinTypeAmenity(models.Model):
    cabin_type = models.ForeignKey(CabinType, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cabin_type', 'amenity')
