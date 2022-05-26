from rest_framework import serializers
from alim.models import Cat, Telephone, Elevage


class CatSerializer(serializers.ModelSerializer):
    """
    serializer for Cat object
    """
    class Meta:
        model = Cat
        fields = ('id',
                  'cat',
                  )
        read_only_fields = ('id',)


class TelephoneSerializer(serializers.ModelSerializer):
    """
    Serializer for telephone object
    """

    class Meta:
        model = Telephone
        fields = (
            'id',
            'user',
            'phone',
            'phonefix',
        )
        read_only_fields = ('user', 'id')


class ElevageSerializer(serializers.ModelSerializer):
    """
    Serializer for Elevage object
    """
    class Meta:
        model = Elevage
        fields = (
            'id',
            'nom',
            'typ_elevage',
            'chef_elev',
            'client',
        )
        read_only_fields = ('id',)
