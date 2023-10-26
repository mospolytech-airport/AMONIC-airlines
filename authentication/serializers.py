from rest_framework import serializers

from authentication.models import User
from role.models import Role
from office.models import Office

class UserSerializer(serializers.ModelSerializer):
    office = serializers.SlugRelatedField(slug_field='title', queryset=Office.objects.all())
    role = serializers.SlugRelatedField(slug_field='title', queryset=Role.objects.all())

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.is_active = True

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
