from rest_framework import serializers
from alim.models import Order, Elevage, Silo, User
from django.contrib.gis.db.models import Q


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order object
    """
    elevagelist = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'elevage',
            'elevagelist',
            'created_by',
            'product',
            'delivery',
        )
        read_only_fields = (
            'id',
            'created_by',
            'date_order'
        )

    def get_elevagelist(self, obj):
        return obj.elevagelist()
