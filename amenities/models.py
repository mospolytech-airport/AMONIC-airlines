from django.db import models

class Amenity(models.Model):
    service = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=19, decimal_places=4)

    def __str__(self):
        return self.service
