from rest_framework import serializers
from alim.models import Cat, Telephone


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
