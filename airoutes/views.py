from rest_framework import viewsets

from airoutes.models import Route
from airoutes.serializers import RouteSerializer


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
