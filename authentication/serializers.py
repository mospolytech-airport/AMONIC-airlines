from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
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

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        try: 
            rep['office'] = instance.office.title
            rep['role'] = instance.role.title
            return rep
        except:
            return rep