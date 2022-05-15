from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from alim.models import Cat, Telephone
from client .serializers import TelephoneSerializer, CatSerializer


class BaseUserAttrViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          ):
    """
    Base viewset for user owned recipe attributes
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(user__isnull=False)

        return queryset.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        """Create a new attribute of user"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """ update an attribute of user """
        serializer.save(user=self.request.user)


class TelephoneViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet,
                       ):
    """Manage telephone in the database"""
    permission_classes = (IsAuthenticated,)
    queryset = Telephone.objects.all()
    serializer_class = TelephoneSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(user__isnull=False)

        return queryset.filter(
            user=self.request.user
        )

    def create(self, request):
        tel = Telephone()
        tel.user = self.request.user
        tel.phone = request.data['phone']
        tel.phonefix = request.data['phonefix']
        tel.save()
        serializer = TelephoneSerializer(tel)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update a user and cat correctly and return it"""
        telephone = self.get_object()
        telephone.phone = request.data['phone']
        telephone.phonefix = request.data['phonefix']
        telephone.save()
        serializer = TelephoneSerializer(telephone)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        telephone = self.get_object()
        telephone.phone = request.data.get('phone', telephone.phone)
        telephone.phonefix = request.data.get('phonefix', telephone.phonefix)
        telephone.save()
        serializer = TelephoneSerializer(telephone)
        return Response(serializer.data)


class CatViewSet(BaseUserAttrViewSet):
    """Manage cat in the database"""
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
