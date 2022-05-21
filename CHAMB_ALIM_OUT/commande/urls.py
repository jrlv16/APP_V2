from django.urls import path, include
from rest_framework.routers import DefaultRouter

from commande import views

router = DefaultRouter()
router.register('commande', views.CommandeViewSet)

app_name = 'commande/'

urlpatterns = [
    path('', include(router.urls))
]
