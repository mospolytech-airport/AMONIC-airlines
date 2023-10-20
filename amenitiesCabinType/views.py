from rest_framework import viewsets

from amenitiesCabinType.models import CabinTypeAmenity
from amenitiesCabinType.serializers import CabinTypeAmenitySerializer


class CabinTypeAmenityViewSet(viewsets.ModelViewSet):
    serializer_class = CabinTypeAmenitySerializer
    queryset = CabinTypeAmenity.objects.all()
