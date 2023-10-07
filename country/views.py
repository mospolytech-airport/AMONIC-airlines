from rest_framework import viewsets

from country.models import Country 
from country.serializers import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
