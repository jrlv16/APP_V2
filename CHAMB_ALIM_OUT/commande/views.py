import datetime
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, viewsets, mixins, generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from alim.models import Order, Elevage, Silo, Chef_elev, Cat, Telephone

from commande.serializers import OrderSerializer
from user.serializers import Chef_elevSerializer


class CommandeViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet,):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    ordering_fields = ['delivery', 'product']
    search_fields = [
        'elevage__nom', 'product__produit', 'elevage__client__last_name']

    def get_user(self):
        """
        Retrieve and return authenticated user
        """
        return self.request.user

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset = self.queryset
        user = self.get_user()
        if user.cat not in ['CLIENT', 'CH_ELE']:
            return queryset.filter(delivered=False)
        elif assigned_only:
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


class Chef_elevViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet,):
    """Create a new Chef_elev"""
    serializer_class = Chef_elevSerializer
    queryset = Chef_elev.objects.all()

    def get_user(self):
        """
        Retrieve and return authenticated user
        """
        return self.request.user

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        if self.request.user.cat not in ['CLIENT', 'CH_ELE']:
            queryset = self.queryset
        else:
            queryset = Chef_elev.objects.all().filter(created_by=self.request.user)
        return queryset

    def create(self, request):
        """Creates chef d'élevage"""
        chef_elev = Chef_elev()
        cat = Cat()
        tel = Telephone()

        cheflist = Chef_elev.objects.all().filter(created_by=self.get_object())
        numchef = len(cheflist)+1
        chef_elev.clientcode = str(
            self.get_object().clientcode + "_"+"chef_elev.first_name"+"_"+str(numchef))
        chef_elev.created_by = self.get_object()
        chef_elev.last_name = request.data['last_name']
        chef_elev.first_name = request.data['first_name']
        chef_elev.societe = self.get_object().societe
        chef_elev.email = request.data['email']
        if not request.data['email']:
            chef_elev.email = str(
                chef_elev.clientcode+"@test.com")
        chef_elev.save()
        tel.user = chef_elev
        telephone = request.data
        tel.phone = telephone['telephone.phone']
        tel.phonefix = telephone['telephone.phonefix']
        tel.save()
        cat.user = chef_elev
        cat.cat = 'CH_ELE'
        cat.save()
        serializer = Chef_elevSerializer(chef_elev)
        return Response(serializer.data)

    def update(self, instance, validated_data):
        """update a Chef_elev and cat correctly and return it"""
        chef_elev = super().update(instance, validated_data)
        Chef_elev.objects.update()
        return chef_elev

    def partial_update(self, request, *args, **kwargs):
        chef_elev = self.get_object()
        chef_elev.last_name = request.data.get(
            'last_name', chef_elev.last_name)
        chef_elev.first_name = request.data.get(
            'first_name', chef_elev.first_name)
        chef_elev.save()
        serializer = Chef_elevSerializer(chef_elev)
        return Response(serializer.data)

        return chef_elev
