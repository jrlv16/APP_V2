from rest_framework import generics, authentication, permissions
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
                    generics.RetrieveAPIView):
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


class CreateChef_elevView(generics.ListCreateAPIView):
    """Create a new Chef_elev"""
    serializer_class = Chef_elevSerializer

    def get_object(self):
        """
        Retrieve and return authenticated user
        """
        user = self.request.user
        return user

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
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
            self.get_object().clientcode + "_"+str(numchef))
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
