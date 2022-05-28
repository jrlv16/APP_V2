from rest_framework import generics, authentication, permissions, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.serializers import (
    UserSerializer, UserCoordSerializer, Chef_elevSerializer)
from client.serializers import TelephoneSerializer, CatSerializer
from alim.models import Telephone, Cat, Chef_elev


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """ Retrieve and return authenticated user"""
        user = self.request.user
        return user


class UserCoordView(generics.CreateAPIView,
                    generics.RetrieveAPIView,
                    generics.UpdateAPIView):
    """
    Manage phone for user, perhaps address later
    """
    serializer_class = UserCoordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Retrieve and return authenticated user
        """
        print(self.request.user)
        return self.request.user

    def create(self, request):
        """
        Creates Telephone for request user
        """

        user = self.get_object()
        tel = Telephone()
        tel.user = user
        telephone = request.data
        tel.phone = telephone['telephone']['phone']
        tel.phonefix = telephone['telephone']['phonefix']
        tel.save()
        serializer = UserCoordSerializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Updates phone for request user
        """
        user = self.get_object()
        telephone = Telephone.objects.get(user=user)

        print(telephone)
        telephone.phone = request.data['telephone']['phone']
        telephone.phonefix = request.data['telephone']['phonefix']
        telephone.save()
        serializer = UserCoordSerializer(user)
        return Response(serializer.data)
