from rest_framework import viewsets

from cabintypes.models import CabinType
from cabintypes.serializers import CabinTypeSerializer


class CabinTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CabinTypeSerializer
    queryset = CabinType.objects.all()
