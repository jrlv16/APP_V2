from django.urls import path, include
from rest_framework.routers import DefaultRouter

from commande import views

router = DefaultRouter()
router.register('commande', views.CommandeViewSet)
router.register('chef_elev', views.Chef_elevViewSet)

app_name = 'commande/'

urlpatterns = [
    path('', include(router.urls))
]
