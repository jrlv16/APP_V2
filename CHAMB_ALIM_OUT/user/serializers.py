from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from alim.models import models
from django.contrib.gis.db.models import Q


class UserSerializer(serializers.ModelSerializer):

    """serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = ('clientcode', 'password', 'societe',
                  'email', 'last_name', 'first_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ Create a new user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    clientcode = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        clientcode = attrs.get('clientcode')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=clientcode,
            password=password
        )
        if not user:
            msg = _("impossible d'authentifier l'utilisateur")
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
