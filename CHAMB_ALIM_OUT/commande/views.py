import datetime
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, viewsets, mixins, generics, filters
from rest_framework.permissions import IsAuthenticated

from alim.models import Order
from commande.serializers import OrderSerializer


class CommandeViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet,):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['-delivery', 'product']

    def get_user(self):
        """
        Retrieve and return authenticated user
        """
        return self.request.user

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(user__isnull=False)

        return queryset.filter(
            created_by=self.request.user
        )

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.recorded or instance.delivered:
            msg = _('commande déja enregistrée ou livrée')
            raise serializers.ValidationError(msg, code='authorization')
        return super().update(request, *args, **kwargs)
