from rest_framework import serializers

from amenitiesCabinType.models import CabinTypeAmenity


class CabinTypeAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinTypeAmenity
        fields = '__all__'
