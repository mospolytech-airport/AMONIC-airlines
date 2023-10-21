from rest_framework import viewsets

from amenities.models import Amenity
from amenities.serializers import AmenitySerializer


class AmenityViewSet(viewsets.ModelViewSet):
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()
