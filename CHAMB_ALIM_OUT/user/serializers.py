from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from alim.models import User, Telephone, Cat, Chef_elev
from django.contrib.gis.db.models import Q
from client.serializers import TelephoneSerializer, CatSerializer


class UserSerializer(serializers.ModelSerializer):

    """serializer for user object"""
    cat = CatSerializer()

    class Meta:
        model = get_user_model()
        fields = ('clientcode', 'password', 'societe',
                  'email', 'last_name', 'first_name', 'cat')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ Create a new user with encrypted password"""
        cat_data = validated_data.pop('cat')
        """on crée un fake de mail pour envoyer le reset password par sms
        en utilisant drf_password_reset, on testera suite au signal de demande
        de renouvellement de mot de passe si fake ou non
        """
        if not validated_data['email']:
            validated_data['email'] = str(
                validated_data['clientcode']+"@test.com")
            print(validated_data['email'])

        user = get_user_model().objects.create_user(**validated_data)
        Cat.objects.create(user=user, **cat_data)
        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        cat_data = validated_data.pop('cat')
        user = super().update(instance, validated_data)
        Cat.objects.update(**cat_data)
        return user


class UserCoordSerializer(serializers.ModelSerializer):
    """
    Serializer for users telephon and adress
    """
    telephone = TelephoneSerializer(many=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'telephone')
        read_only_fields = ('id', 'first_name', 'last_name')


class Chef_elevSerializer(serializers.ModelSerializer):
    """
    Serializer ofr Chef_elev
    """
    telephone = TelephoneSerializer(many=False)

    class Meta:
        model = Chef_elev
        fields = (
            'id',
            'clientcode',
            'email',
            'password',
            'first_name',
            'last_name',
            'telephone',

        )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ('id', 'clientcode', 'created_by')

    def update(self, instance, validated_data):
        """update a Chef_elev and cat correctly and return it"""
        chef_elev = super().update(instance, validated_data)
        Chef_elev.objects.update()
        return chef_elev
