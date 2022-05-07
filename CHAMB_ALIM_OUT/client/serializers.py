from rest_framework import serializers
from alim.models import Cat


class CatSerializer(serializers.ModelSerializer):
    """
    serialzier for Cat object
    """
    class Meta:
        model = Cat
        fields = ('id',
                  'cat',
                  )
        read_only_fields = ('id',)
