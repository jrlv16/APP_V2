from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from alim.models import Cat
from client import serializers


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


class CatViewSet(BaseUserAttrViewSet):
    """Manage cat in the database"""
    queryset = Cat.objects.all()
    serializer_class = serializers.CatSerializer
