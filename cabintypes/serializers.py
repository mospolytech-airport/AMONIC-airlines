from rest_framework import serializers

from cabintypes.models import CabinType


class CabinTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinType
        fields = '__all__'
