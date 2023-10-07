from rest_framework import viewsets

from office.models import Office
from office.serializers import OfficeSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    serializer_class = OfficeSerializer
    queryset = Office.objects.all()
